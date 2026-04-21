from __future__ import annotations

import uuid
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

import pytest
from app.db import SessionLocal
from app.models import Booking, Desk, Room
from app.schema.booking import BookingCreate
from app.services.booking_service import BookingService
from sqlalchemy import select


@pytest.fixture
def two_desks() -> tuple[uuid.UUID, uuid.UUID]:
    with SessionLocal() as session:
        room = Room(
            id=uuid.uuid4(),
            room_number="T-2",
            description="Test room",
            name="T-2 - Test room",
            sort_order=0,
        )
        session.add(room)
        session.flush()
        d1 = Desk(
            id=uuid.uuid4(),
            room_id=room.id,
            name="Desk A",
            bookable=True,
            monitor_count=1,
            has_keyboard=True,
            has_mouse=True,
            sort_order=0,
        )
        d2 = Desk(
            id=uuid.uuid4(),
            room_id=room.id,
            name="Desk B",
            bookable=True,
            monitor_count=1,
            has_keyboard=True,
            has_mouse=True,
            sort_order=1,
        )
        session.add_all([d1, d2])
        session.commit()
        return d1.id, d2.id


def test_create_same_day_after_10_raises(two_desks: tuple[uuid.UUID, uuid.UUID]) -> None:
    desk_id, _ = two_desks
    tz = ZoneInfo("Europe/Berlin")
    today = datetime.now(tz=tz).date()
    now = datetime.combine(today, time(10, 1), tzinfo=tz)

    with SessionLocal() as session:
        svc = BookingService(session)
        with pytest.raises(ValueError, match="same-day bookings are not available"):
            svc.create_booking(
                BookingCreate(
                    desk_id=desk_id,
                    booking_date=today,
                    display_name="test-user",
                ),
                now=now,
            )


def test_two_same_day_bookings_before_cutoff(two_desks: tuple[uuid.UUID, uuid.UUID]) -> None:
    d1, d2 = two_desks
    tz = ZoneInfo("Europe/Berlin")
    today = datetime.now(tz=tz).date()
    now = datetime.combine(today, time(9, 30), tzinfo=tz)

    with SessionLocal() as session:
        svc = BookingService(session)
        svc.create_booking(
            BookingCreate(desk_id=d1, booking_date=today, display_name="a"),
            now=now,
        )
        svc.create_booking(
            BookingCreate(desk_id=d2, booking_date=today, display_name="b"),
            now=now,
        )
        session.commit()

    with SessionLocal() as session:
        rows = session.scalars(
            select(Booking).where(Booking.booking_date == today),
        ).all()
        assert len(rows) == 2


def test_check_in_only_on_booking_day(
    two_desks: tuple[uuid.UUID, uuid.UUID],
) -> None:
    desk_id, _ = two_desks
    tz = ZoneInfo("Europe/Berlin")
    today = datetime.now(tz=tz).date()
    tomorrow = today + timedelta(days=1)
    now_today = datetime.combine(today, time(9, 0), tzinfo=tz)

    with SessionLocal() as session:
        svc = BookingService(session)
        created = svc.create_booking(
            BookingCreate(
                desk_id=desk_id,
                booking_date=tomorrow,
                display_name="future-book",
            ),
            now=now_today,
        )
        session.commit()
        booking_id = created.id

    with SessionLocal() as session:
        svc = BookingService(session)
        with pytest.raises(ValueError, match="check-in only on the booking day"):
            svc.check_in(booking_id, "future-book", now=now_today)
