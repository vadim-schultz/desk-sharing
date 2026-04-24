from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Protocol

from app.models import Room
from app.schema.admin import AdminDeskRead

# Sentinel IDs: never persisted; rows using null slots are skipped before public API output.
NULL_DESK_SLOT_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")
NULL_BOOKING_SLOT_ID = uuid.UUID("00000000-0000-0000-0000-000000000002")


class DeskSlot(Protocol):
    """Desk side of a room listing row (outer join or admin flattening)."""

    @property
    def id(self) -> uuid.UUID: ...

    @property
    def name(self) -> str: ...

    @property
    def bookable(self) -> bool: ...

    @property
    def monitor_count(self) -> int: ...

    @property
    def has_keyboard(self) -> bool: ...

    @property
    def has_mouse(self) -> bool: ...

    @property
    def sort_order(self) -> int: ...

    def participates_in_layout(self) -> bool:
        """False for placeholder rows when a room has no desk in an outer join."""

    def to_admin_desk_read(self) -> AdminDeskRead | None:
        """Null desk returns ``None``; ORM desk returns a read model."""


class BookingSlot(Protocol):
    """Booking side of a room listing row."""

    @property
    def id(self) -> uuid.UUID: ...

    @property
    def checked_in_at(self) -> datetime | None: ...

    def has_reservation_for_day(self) -> bool:
        """False when no booking row exists for the requested day."""


@dataclass(frozen=True, slots=True)
class RoomDayRow:
    room: Room
    desk: DeskSlot
    booking: BookingSlot


class _NullDesk:
    __slots__ = ()

    @property
    def id(self) -> uuid.UUID:
        return NULL_DESK_SLOT_ID

    @property
    def name(self) -> str:
        return ""

    @property
    def bookable(self) -> bool:
        return False

    @property
    def monitor_count(self) -> int:
        return 0

    @property
    def has_keyboard(self) -> bool:
        return False

    @property
    def has_mouse(self) -> bool:
        return False

    @property
    def sort_order(self) -> int:
        return 0

    def participates_in_layout(self) -> Literal[False]:
        return False

    def to_admin_desk_read(self) -> None:
        return None


class _NullBooking:
    __slots__ = ()

    @property
    def id(self) -> uuid.UUID:
        return NULL_BOOKING_SLOT_ID

    @property
    def checked_in_at(self) -> None:
        return None

    def has_reservation_for_day(self) -> Literal[False]:
        return False


NULL_DESK: DeskSlot = _NullDesk()
NULL_BOOKING: BookingSlot = _NullBooking()
