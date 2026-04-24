from __future__ import annotations

import uuid
from datetime import date, datetime, time
from zoneinfo import ZoneInfo

from app.db import SessionLocal
from app.models import Booking, Desk, Room
from app.services.maintenance import release_stale_pending_bookings


def test_release_stale_pending_deletes_expired() -> None:
    tz = ZoneInfo("Europe/Berlin")
    d = date(2026, 4, 10)
    now = datetime.combine(d, time(10, 30), tzinfo=tz)

    with SessionLocal() as session:
        room = Room(
            id=uuid.uuid4(),
            room_number="M-1",
            description="",
            name="M-1",
            sort_order=0,
        )
        session.add(room)
        session.flush()
        desk = Desk(
            id=uuid.uuid4(),
            room_id=room.id,
            name="D1",
            bookable=True,
            monitor_count=0,
            has_keyboard=False,
            has_mouse=False,
            sort_order=0,
        )
        session.add(desk)
        session.flush()
        b = Booking(
            id=uuid.uuid4(),
            desk_id=desk.id,
            booking_date=d,
            display_name="x",
            checked_in_at=None,
            created_at=datetime.combine(d, time(8, 0), tzinfo=tz),
        )
        session.add(b)
        session.commit()
        booking_id = b.id

    with SessionLocal() as session:
        n = release_stale_pending_bookings(session, now=now)
        assert n == 1
        session.commit()

    with SessionLocal() as session:
        assert session.get(Booking, booking_id) is None
