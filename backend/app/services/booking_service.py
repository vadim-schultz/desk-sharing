from __future__ import annotations

import uuid
from datetime import date, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.config import settings
from app.models import Booking, Desk, Room
from app.schema.booking import BookingCreate, BookingCreated
from app.schema.desk import DeskRead
from app.schema.enums import DeskDayStatus
from app.schema.room import RoomRead
from app.timeutil import (
    get_zone,
    is_booking_date_allowed,
    is_pending_release,
    today_in_zone,
)


class BookingService:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._tz = get_zone(settings.app_timezone)

    def release_stale_pending(self, now: datetime | None = None) -> int:
        """Delete unchecked bookings past 10:00 on their booking day. Returns count deleted."""
        if now is None:
            now = datetime.now(tz=self._tz)
        elif now.tzinfo is None:
            msg = "now must be timezone-aware"
            raise ValueError(msg)
        pending = self._session.scalars(
            select(Booking).where(Booking.checked_in_at.is_(None))
        ).all()
        deleted = 0
        for b in pending:
            if is_pending_release(
                booking_date=b.booking_date,
                checked_in_at=None,
                now=now,
                tz=self._tz,
            ):
                self._session.delete(b)
                deleted += 1
        return deleted

    def list_rooms_for_date(
        self, view_date: date | None, now: datetime | None = None
    ) -> tuple[date, list[RoomRead]]:
        if now is None:
            now = datetime.now(tz=self._tz)
        elif now.tzinfo is None:
            msg = "now must be timezone-aware"
            raise ValueError(msg)

        self.release_stale_pending(now=now)

        day = view_date if view_date is not None else today_in_zone(self._tz, now=now)

        rooms = list(
            self._session.scalars(
                select(Room)
                .options(joinedload(Room.desks))
                .order_by(Room.sort_order, Room.room_number, Room.name)
            ).unique()
        )

        result: list[RoomRead] = []
        for room in rooms:
            desks_out: list[DeskRead] = []
            for desk in sorted(room.desks, key=lambda d: (d.sort_order, d.name)):
                booking = self._session.scalar(
                    select(Booking).where(
                        Booking.desk_id == desk.id,
                        Booking.booking_date == day,
                    )
                )
                status, booking_id = self._desk_status(desk, booking)
                desks_out.append(
                    DeskRead(
                        id=desk.id,
                        name=desk.name,
                        bookable=desk.bookable,
                        monitor_count=desk.monitor_count,
                        has_keyboard=desk.has_keyboard,
                        has_mouse=desk.has_mouse,
                        status=status,
                        booking_id=booking_id,
                    )
                )
            result.append(
                RoomRead(
                    id=room.id,
                    room_number=room.room_number,
                    description=room.description,
                    name=room.name,
                    desks=desks_out,
                )
            )
        return day, result

    def _desk_status(
        self, desk: Desk, booking: Booking | None
    ) -> tuple[DeskDayStatus, uuid.UUID | None]:
        if not desk.bookable:
            return DeskDayStatus.unavailable, None
        if booking is None:
            return DeskDayStatus.bookable, None
        if booking.checked_in_at is not None:
            return DeskDayStatus.booked, booking.id
        return DeskDayStatus.pending, booking.id

    def create_booking(self, data: BookingCreate, now: datetime | None = None) -> BookingCreated:
        if now is None:
            now = datetime.now(tz=self._tz)
        elif now.tzinfo is None:
            msg = "now must be timezone-aware"
            raise ValueError(msg)

        self.release_stale_pending(now=now)
        today = today_in_zone(self._tz, now=now)
        if not is_booking_date_allowed(data.booking_date, today, max_ahead=5):
            msg = "booking_date is outside the allowed window"
            raise ValueError(msg)

        desk = self._session.get(Desk, data.desk_id)
        if desk is None or not desk.bookable:
            msg = "desk is not bookable"
            raise ValueError(msg)

        existing = self._session.scalar(
            select(Booking).where(
                Booking.desk_id == data.desk_id,
                Booking.booking_date == data.booking_date,
            )
        )
        if existing is not None:
            msg = "desk already has a booking for that date"
            raise ValueError(msg)

        booking = Booking(
            desk_id=data.desk_id,
            booking_date=data.booking_date,
            display_name=data.display_name.strip(),
            checked_in_at=None,
            created_at=now,
        )
        self._session.add(booking)
        self._session.flush()
        return BookingCreated(
            id=booking.id,
            desk_id=booking.desk_id,
            booking_date=booking.booking_date,
            display_name=booking.display_name,
        )

    def check_in(
        self,
        booking_id: uuid.UUID,
        display_name: str,
        now: datetime | None = None,
    ) -> BookingCreated:
        if now is None:
            now = datetime.now(tz=self._tz)
        elif now.tzinfo is None:
            msg = "now must be timezone-aware"
            raise ValueError(msg)

        self.release_stale_pending(now=now)

        booking = self._session.get(Booking, booking_id)
        if booking is None:
            msg = "booking not found"
            raise ValueError(msg)
        if booking.checked_in_at is not None:
            msg = "already checked in"
            raise ValueError(msg)
        if booking.display_name.strip() != display_name.strip():
            msg = "display name does not match"
            raise ValueError(msg)
        if is_pending_release(
            booking_date=booking.booking_date,
            checked_in_at=None,
            now=now,
            tz=self._tz,
        ):
            msg = "check-in window closed"
            raise ValueError(msg)

        booking.checked_in_at = now
        self._session.flush()
        return BookingCreated(
            id=booking.id,
            desk_id=booking.desk_id,
            booking_date=booking.booking_date,
            display_name=booking.display_name,
        )
