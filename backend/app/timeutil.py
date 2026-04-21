from __future__ import annotations

from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo


def get_zone(tz_name: str) -> ZoneInfo:
    return ZoneInfo(tz_name)


def today_in_zone(tz: ZoneInfo, now: datetime | None = None) -> date:
    if now is None:
        now = datetime.now(tz=tz)
    elif now.tzinfo is None:
        msg = "now must be timezone-aware"
        raise ValueError(msg)
    else:
        now = now.astimezone(tz)
    return now.date()


def booking_horizon_end(today: date, days_ahead: int = 5) -> date:
    """Last bookable calendar day: `today + days_ahead` (inclusive window)."""
    return today + timedelta(days=days_ahead)


def is_pending_release(
    *,
    booking_date: date,
    checked_in_at: datetime | None,
    now: datetime,
    tz: ZoneInfo,
) -> bool:
    """True if booking is unchecked and past the 10:00 cutoff on the booking day."""
    if checked_in_at is not None:
        return False
    cutoff_local = datetime.combine(booking_date, time(10, 0), tzinfo=tz)
    if now.tzinfo is None:
        msg = "now must be timezone-aware"
        raise ValueError(msg)
    now_local = now.astimezone(tz)
    return now_local > cutoff_local


def is_past_same_day_booking_cutoff(now: datetime, tz: ZoneInfo) -> bool:
    """True if local time is past 10:00 on today's calendar date in tz."""
    if now.tzinfo is None:
        msg = "now must be timezone-aware"
        raise ValueError(msg)
    today = today_in_zone(tz, now=now)
    return is_pending_release(
        booking_date=today,
        checked_in_at=None,
        now=now,
        tz=tz,
    )


def is_booking_date_allowed(booking_date: date, today: date, max_ahead: int = 5) -> bool:
    last = booking_horizon_end(today, max_ahead)
    return today <= booking_date <= last
