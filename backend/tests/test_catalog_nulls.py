from __future__ import annotations

import uuid
from datetime import date, datetime
from zoneinfo import ZoneInfo

from app.db import SessionLocal
from app.domain.room_listing_slots import (
    NULL_BOOKING,
    NULL_BOOKING_SLOT_ID,
    NULL_DESK,
    NULL_DESK_SLOT_ID,
)
from app.models import Desk, Room
from app.repositories import RoomRepository
from app.schema.enums import DeskDayStatus
from app.schema.list_query import RoomListFilter, RoomListQuery, RoomListSort
from app.services.room_catalog_service import RoomCatalogService
from freezegun import freeze_time
from litestar import Litestar
from litestar.testing import TestClient


def test_null_desk_slot_protocol_defaults() -> None:
    assert NULL_DESK.id == NULL_DESK_SLOT_ID
    assert NULL_DESK.name == ""
    assert NULL_DESK.bookable is False
    assert NULL_DESK.monitor_count == 0
    assert NULL_DESK.has_keyboard is False
    assert NULL_DESK.has_mouse is False
    assert NULL_DESK.sort_order == 0
    assert NULL_DESK.participates_in_layout() is False
    assert NULL_DESK.to_admin_desk_read() is None


def test_null_booking_slot_protocol_defaults() -> None:
    assert NULL_BOOKING.id == NULL_BOOKING_SLOT_ID
    assert NULL_BOOKING.checked_in_at is None
    assert NULL_BOOKING.has_reservation_for_day() is False


def test_desk_model_listing_protocol() -> None:
    with SessionLocal() as session:
        room = Room(
            id=uuid.uuid4(),
            room_number="X",
            description="",
            name="X",
            sort_order=0,
        )
        session.add(room)
        session.flush()
        desk = Desk(
            id=uuid.uuid4(),
            room_id=room.id,
            name="D1",
            bookable=True,
            monitor_count=2,
            has_keyboard=True,
            has_mouse=False,
            sort_order=1,
        )
        session.add(desk)
        session.commit()
        assert desk.participates_in_layout() is True
        read = desk.to_admin_desk_read()
        assert read is not None
        assert read.id == desk.id
        assert read.name == "D1"
        assert read.monitor_count == 2


def test_booking_model_has_reservation() -> None:
    from app.models import Booking

    b = Booking(
        id=uuid.uuid4(),
        desk_id=uuid.uuid4(),
        booking_date=datetime.now(tz=ZoneInfo("UTC")).date(),
        display_name="n",
        checked_in_at=None,
        created_at=datetime.now(tz=ZoneInfo("UTC")),
    )
    assert b.has_reservation_for_day() is True


def test_room_catalog_desk_status_with_null_booking() -> None:
    svc = RoomCatalogService(RoomRepository(SessionLocal()))
    room_id = uuid.uuid4()
    with SessionLocal() as session:
        room = Room(
            id=room_id,
            room_number="Y",
            description="",
            name="Y",
            sort_order=0,
        )
        session.add(room)
        session.flush()
        desk = Desk(
            id=uuid.uuid4(),
            room_id=room_id,
            name="D",
            bookable=True,
            monitor_count=0,
            has_keyboard=False,
            has_mouse=False,
            sort_order=0,
        )
        session.add(desk)
        session.commit()
        status, bid = svc._desk_status(desk, NULL_BOOKING)
        assert status == DeskDayStatus.bookable
        assert bid is None

        status2, _bid2 = svc._desk_status(desk, NULL_BOOKING)
        assert status2 == DeskDayStatus.bookable

    unavail = Desk(
        id=uuid.uuid4(),
        room_id=room_id,
        name="U",
        bookable=False,
        monitor_count=0,
        has_keyboard=False,
        has_mouse=False,
        sort_order=0,
    )
    status3, bid3 = svc._desk_status(unavail, NULL_BOOKING)
    assert status3 == DeskDayStatus.unavailable
    assert bid3 is None


def test_list_rooms_join_normalizes_null_slots() -> None:
    with SessionLocal() as session:
        room = Room(
            id=uuid.uuid4(),
            room_number="Z",
            description="",
            name="Z",
            sort_order=0,
        )
        session.add(room)
        session.commit()
        repo = RoomRepository(session)
        q = RoomListQuery(
            filter=RoomListFilter(booking_date=date(2026, 6, 1)),
            sort=RoomListSort(sort_by="sort_order", sort_order="asc"),
        )
        rows = repo.list_rooms(q)
        assert len(rows) == 1
        assert rows[0].room.id == room.id
        assert rows[0].desk is NULL_DESK
        assert rows[0].booking is NULL_BOOKING


def _admin_token(client: TestClient[Litestar]) -> str:
    r = client.post("/auth/token", json={"password": "dresden"})
    assert r.status_code == 200, r.text
    return str(r.json()["access_token"])


@freeze_time(
    lambda: datetime(2026, 4, 15, 8, 0, 0, tzinfo=ZoneInfo("Europe/Berlin")),
)
def test_public_rooms_room_without_desks_empty_desk_array(
    client: TestClient[Litestar],
) -> None:
    token = _admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    create = client.post(
        "/admin/rooms",
        headers=headers,
        json={"room_number": "ND-1", "description": "No desks", "name": "ND-1"},
    )
    assert create.status_code == 201, create.text
    tz = ZoneInfo("Europe/Berlin")
    book_day = datetime.now(tz=tz).date()
    r = client.get("/rooms", params={"date": book_day.isoformat()})
    assert r.status_code == 200, r.text
    rooms = r.json()["rooms"]
    assert len(rooms) >= 1
    empty_room = next(x for x in rooms if x["room_number"] == "ND-1")
    assert empty_room["desks"] == []
