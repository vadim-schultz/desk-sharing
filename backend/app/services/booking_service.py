from __future__ import annotations

import uuid
from datetime import datetime

from app.config import settings
from app.models import Booking
from app.repositories import BookingRepository, DeskRepository
from app.schema.booking import (
    BookingCreate,
    BookingCreated,
    BookingCreatePreconditions,
    BookingGetFilter,
    CheckInPreconditions,
)
from app.timeutil import get_zone, today_in_zone


class BookingService:
    def __init__(
        self,
        booking_repo: BookingRepository,
        desk_repo: DeskRepository,
    ) -> None:
        self._bookings = booking_repo
        self._desks = desk_repo
        self._tz = get_zone(settings.app_timezone)

    def _aware_now(self, now: datetime | None) -> datetime:
        if now is None:
            return datetime.now(tz=self._tz)
        if now.tzinfo is None:
            msg = "now must be timezone-aware"
            raise ValueError(msg)
        return now

    def create_booking(self, data: BookingCreate, now: datetime | None = None) -> BookingCreated:
        now = self._aware_now(now)
        today = today_in_zone(self._tz, now=now)
        desk = self._desks.get(data.desk_id)
        existing = self._bookings.get(
            BookingGetFilter(desk_id=data.desk_id, booking_date=data.booking_date)
        )
        BookingCreatePreconditions(
            booking_date=data.booking_date,
            now=now,
            today=today,
            tz=self._tz,
            desk_present=desk is not None,
            desk_bookable=bool(desk and desk.bookable),
            existing_booking_present=existing is not None,
        )
        booking = Booking(
            desk_id=data.desk_id,
            booking_date=data.booking_date,
            display_name=data.display_name,
            checked_in_at=None,
            created_at=now,
        )
        self._bookings.add(booking)
        self._bookings.flush()
        return BookingCreated(
            id=booking.id,
            desk_id=booking.desk_id,
            booking_date=booking.booking_date,
            display_name=booking.display_name,
        )

    def check_in(
        self,
        booking_id: uuid.UUID,
        display_name: str,
        now: datetime | None = None,
    ) -> BookingCreated:
        now = self._aware_now(now)
        today = today_in_zone(self._tz, now=now)
        booking = self._bookings.get(BookingGetFilter(booking_id=booking_id))
        CheckInPreconditions(
            booking=booking,
            display_name=display_name,
            now=now,
            today=today,
            tz=self._tz,
        )
        assert booking is not None
        booking.checked_in_at = now
        self._bookings.flush()
        return BookingCreated(
            id=booking.id,
            desk_id=booking.desk_id,
            booking_date=booking.booking_date,
            display_name=booking.display_name,
        )
