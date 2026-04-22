from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session, selectinload

from app.models import Booking, Desk, Room


class RoomRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_rooms_with_desk_booking_for_date(
        self, day: date
    ) -> list[tuple[Room, Desk | None, Booking | None]]:
        """All rooms, left-joined to desks, left-joined to the booking for ``day`` (if any)."""
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
                Room.sort_order,
                Room.room_number,
                Room.name,
                Desk.sort_order,
                Desk.name,
            )
        )
        return [(r[0], r[1], r[2]) for r in self._session.execute(q)]

    def find_all(self) -> list[Room]:
        stmt = (
            select(Room)
            .options(selectinload(Room.desks))
            .order_by(Room.sort_order, Room.room_number, Room.name)
        )
        return list(self._session.scalars(stmt))

    def get(self, room_id: uuid.UUID) -> Room | None:
        stmt = (
            select(Room)
            .options(selectinload(Room.desks))
            .where(Room.id == room_id)
        )
        return self._session.scalar(stmt)

    def add(self, room: Room) -> None:
        self._session.add(room)

    def delete(self, room: Room) -> None:
        self._session.delete(room)

    def max_sort_order(self) -> int | None:
        return self._session.scalar(select(func.max(Room.sort_order)))
