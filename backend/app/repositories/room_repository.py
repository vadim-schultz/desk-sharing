from __future__ import annotations

import uuid
from datetime import date
from typing import Any, cast

from sqlalchemy import ColumnElement, and_, func, select
from sqlalchemy.orm import Session, selectinload

from app.domain.room_listing_slots import NULL_BOOKING, NULL_DESK, RoomDayRow
from app.models import Booking, Desk, Room
from app.schema.list_query import RoomListQuery, RoomListSort


def _room_primary_order(sort: RoomListSort) -> ColumnElement[Any]:
    col = getattr(Room, sort.sort_by)
    return cast(
        "ColumnElement[Any]",
        col.asc() if sort.sort_order == "asc" else col.desc(),
    )


class RoomRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_rooms(self, query: RoomListQuery) -> list[RoomDayRow]:
        """List rooms as flat rows; always returns ``RoomDayRow`` (join or admin flattening)."""
        day = query.filter.booking_date
        if day is not None:
            return self._list_joined_for_booking_day(day, query.sort)
        stmt = (
            select(Room).options(selectinload(Room.desks)).order_by(_room_primary_order(query.sort))
        )
        rooms = list(self._session.scalars(stmt))
        rows: list[RoomDayRow] = []
        for room in rooms:
            if not room.desks:
                rows.append(RoomDayRow(room=room, desk=NULL_DESK, booking=NULL_BOOKING))
            else:
                for desk in room.desks:
                    rows.append(RoomDayRow(room=room, desk=desk, booking=NULL_BOOKING))
        return rows

    def _list_joined_for_booking_day(self, day: date, sort: RoomListSort) -> list[RoomDayRow]:
        q = (
            select(Room, Desk, Booking)
            .select_from(Room)
            .outerjoin(Desk, Room.id == Desk.room_id)
            .outerjoin(
                Booking,
                and_(
                    Booking.desk_id == Desk.id,
                    Booking.booking_date == day,
                ),
            )
            .order_by(
                _room_primary_order(sort),
                Desk.sort_order.asc(),
                Desk.name.asc(),
            )
        )
        return [
            RoomDayRow(
                room=r[0],
                desk=r[1] if r[1] is not None else NULL_DESK,
                booking=r[2] if r[2] is not None else NULL_BOOKING,
            )
            for r in self._session.execute(q)
        ]

    def get(self, room_id: uuid.UUID) -> Room | None:
        stmt = select(Room).options(selectinload(Room.desks)).where(Room.id == room_id)
        return self._session.scalar(stmt)

    def add(self, room: Room) -> None:
        self._session.add(room)

    def delete(self, room: Room) -> None:
        self._session.delete(room)

    def max_sort_order(self) -> int | None:
        return self._session.scalar(select(func.max(Room.sort_order)))
