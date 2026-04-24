from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from app.config import settings
from app.repositories import BookingRepository
from app.schema.booking import BookingListFilter
from app.timeutil import get_zone, is_pending_release


def release_stale_pending_bookings(
    session: Session, now: datetime | None = None
) -> int:
    """Delete unchecked bookings past the release cutoff on their booking day."""
    tz = get_zone(settings.app_timezone)
    if now is None:
        now = datetime.now(tz=tz)
    elif now.tzinfo is None:
        msg = "now must be timezone-aware"
        raise ValueError(msg)

    bookings = BookingRepository(session)
    deleted = 0
    for b in bookings.list(BookingListFilter(checked_in="pending")):
        if is_pending_release(
            booking_date=b.booking_date,
            checked_in_at=None,
            now=now,
            tz=tz,
        ):
            bookings.delete(b)
            deleted += 1
    return deleted
