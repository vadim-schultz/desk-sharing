from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Booking


class BookingRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_unchecked_bookings(self) -> list[Booking]:
        return list(
            self._session.scalars(
                select(Booking).where(Booking.checked_in_at.is_(None))
            ).all()
        )

    def get_by_desk_and_date(
        self, desk_id: uuid.UUID, booking_date: date
    ) -> Booking | None:
        return self._session.scalar(
            select(Booking).where(
                Booking.desk_id == desk_id,
                Booking.booking_date == booking_date,
            )
        )

    def get_by_id(self, booking_id: uuid.UUID) -> Booking | None:
        return self._session.get(Booking, booking_id)

    def add(self, booking: Booking) -> None:
        self._session.add(booking)

    def delete(self, booking: Booking) -> None:
        self._session.delete(booking)

    def flush(self) -> None:
        self._session.flush()
