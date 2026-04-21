from __future__ import annotations

from enum import StrEnum


class DeskDayStatus(StrEnum):
    unavailable = "unavailable"
    bookable = "bookable"
    pending = "pending"
    booked = "booked"
