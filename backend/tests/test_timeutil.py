from __future__ import annotations

from datetime import date, datetime
from zoneinfo import ZoneInfo

from app.timeutil import (
    booking_horizon_end,
    is_booking_date_allowed,
    is_pending_release,
    today_in_zone,
)


def test_today_in_zone() -> None:
    tz = ZoneInfo("Europe/Berlin")
    now = datetime(2026, 4, 21, 15, 30, tzinfo=tz)
    assert today_in_zone(tz, now=now) == date(2026, 4, 21)


def test_booking_horizon() -> None:
    today = date(2026, 4, 21)
    assert booking_horizon_end(today, 5) == date(2026, 4, 26)


def test_is_booking_date_allowed() -> None:
    today = date(2026, 4, 21)
    assert is_booking_date_allowed(date(2026, 4, 21), today) is True
    assert is_booking_date_allowed(date(2026, 4, 26), today) is True
    assert is_booking_date_allowed(date(2026, 4, 27), today) is False
    assert is_booking_date_allowed(date(2026, 4, 20), today) is False


def test_pending_release_after_cutoff() -> None:
    tz = ZoneInfo("Europe/Berlin")
    d = date(2026, 4, 21)
    now = datetime(2026, 4, 21, 11, 0, tzinfo=tz)
    assert is_pending_release(booking_date=d, checked_in_at=None, now=now, tz=tz) is True


def test_pending_release_before_cutoff() -> None:
    tz = ZoneInfo("Europe/Berlin")
    d = date(2026, 4, 21)
    now = datetime(2026, 4, 21, 9, 30, tzinfo=tz)
    assert is_pending_release(booking_date=d, checked_in_at=None, now=now, tz=tz) is False


def test_naive_now_rejected() -> None:
    tz = ZoneInfo("Europe/Berlin")
    try:
        is_pending_release(
            booking_date=date(2026, 4, 21),
            checked_in_at=None,
            now=datetime(2026, 4, 21, 11, 0),  # noqa: DTZ001
            tz=tz,
        )
    except ValueError:
        return
    raise AssertionError
