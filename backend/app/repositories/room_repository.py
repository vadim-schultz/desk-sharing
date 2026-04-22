from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

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

    def get_desk(self, desk_id: uuid.UUID) -> Desk | None:
        return self._session.get(Desk, desk_id)
