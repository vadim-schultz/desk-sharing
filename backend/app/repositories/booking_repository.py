from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Booking
from app.schema.booking import BookingGetFilter, BookingListFilter


class BookingRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list(self, flt: BookingListFilter) -> list[Booking]:
        q = select(Booking)
        if flt.checked_in == "pending":
            q = q.where(Booking.checked_in_at.is_(None))
        elif flt.checked_in == "done":
            q = q.where(Booking.checked_in_at.isnot(None))
        return list(self._session.scalars(q).all())

    def get(self, flt: BookingGetFilter) -> Booking | None:
        if flt.booking_id is not None:
            return self._session.get(Booking, flt.booking_id)
        return self._session.scalar(
            select(Booking).where(
                Booking.desk_id == flt.desk_id,
                Booking.booking_date == flt.booking_date,
            )
        )

    def add(self, booking: Booking) -> None:
        self._session.add(booking)

    def delete(self, booking: Booking) -> None:
        self._session.delete(booking)

    def flush(self) -> None:
        self._session.flush()
