from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Annotated, Literal, Self
from zoneinfo import ZoneInfo

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, model_validator

from app.models import Booking
from app.schema.room import RoomRead
from app.timeutil import (
    is_booking_date_allowed,
    is_past_same_day_booking_cutoff,
    is_pending_release,
)


def _strip_str(v: object) -> object:
    if isinstance(v, str):
        return v.strip()
    return v


StrippedDisplayName = Annotated[str, BeforeValidator(_strip_str)]


class BookingGetFilter(BaseModel):
    """Resolve a single booking by id or by desk + calendar date."""

    booking_id: uuid.UUID | None = None
    desk_id: uuid.UUID | None = None
    booking_date: date | None = None

    @model_validator(mode="after")
    def _forbid_booking_id_with_desk_id(self) -> Self:
        if self.booking_id is not None and self.desk_id is not None:
            msg = "Provide either booking_id or desk_id with booking_date, not both"
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def _forbid_booking_id_with_booking_date(self) -> Self:
        if self.booking_id is not None and self.booking_date is not None:
            msg = "Provide either booking_id or desk_id with booking_date, not both"
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def _desk_id_and_booking_date_must_be_paired(self) -> Self:
        if self.desk_id is None and self.booking_date is None:
            return self
        if self.desk_id is not None and self.booking_date is not None:
            return self
        msg = "desk_id and booking_date must be provided together"
        raise ValueError(msg)

    @model_validator(mode="after")
    def _require_booking_id_or_desk_with_date(self) -> Self:
        if self.booking_id is not None:
            return self
        if self.desk_id is not None and self.booking_date is not None:
            return self
        msg = "Provide booking_id or desk_id and booking_date"
        raise ValueError(msg)


class BookingListFilter(BaseModel):
    """Narrow bookings by check-in state."""

    checked_in: Literal["any", "pending", "done"] = "any"


class BookingCreate(BaseModel):
    desk_id: uuid.UUID
    booking_date: date
    display_name: StrippedDisplayName = Field(..., min_length=1, max_length=200)


class BookingCreatePreconditions(BaseModel):
    """Resolved facts before insert; raises ``ValueError`` with a stable message if invalid."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    booking_date: date
    now: datetime
    today: date
    tz: ZoneInfo
    desk_present: bool
    desk_bookable: bool
    existing_booking_present: bool

    @model_validator(mode="after")
    def _booking_date_must_be_within_allowed_window(self) -> Self:
        if not is_booking_date_allowed(self.booking_date, self.today, max_ahead=5):
            msg = "booking_date is outside the allowed window"
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def _same_day_booking_must_respect_cutoff(self) -> Self:
        if self.booking_date == self.today and is_past_same_day_booking_cutoff(
            self.now, self.tz
        ):
            msg = "same-day bookings are not available after 10:00"
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def _desk_must_be_bookable(self) -> Self:
        if not self.desk_present or not self.desk_bookable:
            msg = "desk is not bookable"
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def _desk_must_not_already_be_booked(self) -> Self:
        if self.existing_booking_present:
            msg = "desk already has a booking for that date"
            raise ValueError(msg)
        return self


class CheckInPreconditions(BaseModel):
    """Validates check-in against loaded booking and clock context."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    booking: Booking | None
    display_name: str
    now: datetime
    today: date
    tz: ZoneInfo

    @model_validator(mode="after")
    def _booking_must_exist(self) -> Self:
        if self.booking is None:
            msg = "booking not found"
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def _booking_must_not_already_be_checked_in(self) -> Self:
        if self.booking is not None and self.booking.checked_in_at is not None:
            msg = "already checked in"
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def _display_name_must_match(self) -> Self:
        if self.booking is None:
            return self
        if self.booking.display_name.strip() != self.display_name.strip():
            msg = "display name does not match"
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def _check_in_must_be_on_booking_day(self) -> Self:
        if self.booking is None:
            return self
        if self.booking.booking_date != self.today:
            msg = "check-in only on the booking day"
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def _check_in_must_not_be_past_release_window(self) -> Self:
        if self.booking is None:
            return self
        if is_pending_release(
            booking_date=self.booking.booking_date,
            checked_in_at=None,
            now=self.now,
            tz=self.tz,
        ):
            msg = "check-in window closed"
            raise ValueError(msg)
        return self


class BookingCreated(BaseModel):
    id: uuid.UUID
    desk_id: uuid.UUID
    booking_date: date
    display_name: str


class CheckInRequest(BaseModel):
    display_name: StrippedDisplayName = Field(..., min_length=1, max_length=200)


class RoomsWithStatusResponse(BaseModel):
    date: date
    timezone: str
    rooms: list[RoomRead]
