from __future__ import annotations

import uuid
from datetime import date
from typing import Any, cast

from sqlalchemy import ColumnElement, and_, func, select
from sqlalchemy.orm import Session, selectinload

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

    def list_rooms(
        self, query: RoomListQuery
    ) -> list[Room] | list[tuple[Room, Desk | None, Booking | None]]:
        """List rooms; shape depends on ``query.filter.booking_date`` (see ``RoomListFilter``)."""
        day = query.filter.booking_date
        if day is not None:
            return self._list_joined_for_booking_day(day, query.sort)
        stmt = (
            select(Room).options(selectinload(Room.desks)).order_by(_room_primary_order(query.sort))
        )
        return list(self._session.scalars(stmt))

    def _list_joined_for_booking_day(
        self, day: date, sort: RoomListSort
    ) -> list[tuple[Room, Desk | None, Booking | None]]:
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
        return [(r[0], r[1], r[2]) for r in self._session.execute(q)]

    def get(self, room_id: uuid.UUID) -> Room | None:
        stmt = select(Room).options(selectinload(Room.desks)).where(Room.id == room_id)
        return self._session.scalar(stmt)

    def add(self, room: Room) -> None:
        self._session.add(room)

    def delete(self, room: Room) -> None:
        self._session.delete(room)

    def max_sort_order(self) -> int | None:
        return self._session.scalar(select(func.max(Room.sort_order)))
