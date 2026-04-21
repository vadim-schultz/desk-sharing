from __future__ import annotations

import uuid
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest
from app.db import SessionLocal
from app.models import Desk, Room
from litestar import Litestar
from litestar.testing import TestClient


@pytest.fixture
def room_desk() -> tuple[uuid.UUID, uuid.UUID]:
    with SessionLocal() as session:
        room = Room(
            id=uuid.uuid4(),
            room_number="T-1",
            description="Test room",
            name="T-1 - Test room",
            sort_order=0,
        )
        session.add(room)
        session.flush()
        desk = Desk(
            id=uuid.uuid4(),
            room_id=room.id,
            name="Desk 1",
            bookable=True,
            monitor_count=1,
            has_keyboard=True,
            has_mouse=True,
            sort_order=0,
        )
        session.add(desk)
        session.commit()
        return room.id, desk.id


def test_health(client: TestClient[Litestar]) -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_list_rooms_empty(client: TestClient[Litestar]) -> None:
    r = client.get("/rooms")
    assert r.status_code == 200
    body = r.json()
    assert body["rooms"] == []
    assert "date" in body
    assert body["timezone"] == "Europe/Berlin"


def test_booking_flow(
    client: TestClient[Litestar],
    room_desk: tuple[uuid.UUID, uuid.UUID],
) -> None:
    _room_id, desk_id = room_desk
    tz = ZoneInfo("Europe/Berlin")
    today = datetime.now(tz=tz).date()
    # Book tomorrow so GET /rooms does not release pending (same calendar day + past 10:00).
    book_day = today + timedelta(days=1)

    r = client.get("/rooms", params={"booking_date": book_day.isoformat()})
    assert r.status_code == 200
    desk_payload = r.json()["rooms"][0]["desks"][0]
    assert desk_payload["status"] == "bookable"

    create = client.post(
        "/bookings",
        json={
            "desk_id": str(desk_id),
            "booking_date": book_day.isoformat(),
            "display_name": "curious-mouse-123",
        },
    )
    assert create.status_code == 201, create.text
    booking_id = create.json()["id"]

    r2 = client.get("/rooms", params={"booking_date": book_day.isoformat()})
    assert r2.json()["rooms"][0]["desks"][0]["status"] == "pending"

    check = client.post(
        f"/bookings/{booking_id}/check-in",
        json={"display_name": "curious-mouse-123"},
    )
    assert check.status_code == 201, check.text

    r3 = client.get("/rooms", params={"booking_date": book_day.isoformat()})
    assert r3.json()["rooms"][0]["desks"][0]["status"] == "booked"
