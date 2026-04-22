from __future__ import annotations

import uuid
from datetime import date, datetime

from app.config import settings
from app.models import Booking, Desk, Room
from app.repositories import BookingRepository, RoomRepository
from app.schema.booking import BookingCreate, BookingCreated
from app.schema.desk import DeskRead
from app.schema.enums import DeskDayStatus
from app.schema.room import RoomRead
from app.timeutil import (
    get_zone,
    is_booking_date_allowed,
    is_past_same_day_booking_cutoff,
    is_pending_release,
    today_in_zone,
)


class BookingService:
    def __init__(self, room_repo: RoomRepository, booking_repo: BookingRepository) -> None:
        self._rooms = room_repo
        self._bookings = booking_repo
        self._tz = get_zone(settings.app_timezone)

    def release_stale_pending(self, now: datetime | None = None) -> int:
        """Delete unchecked bookings past 10:00 on their booking day. Returns count deleted."""
        if now is None:
            now = datetime.now(tz=self._tz)
        elif now.tzinfo is None:
            msg = "now must be timezone-aware"
            raise ValueError(msg)
        pending = self._bookings.list_unchecked_bookings()
        deleted = 0
        for b in pending:
            if is_pending_release(
                booking_date=b.booking_date,
                checked_in_at=None,
                now=now,
                tz=self._tz,
            ):
                self._bookings.delete(b)
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

        day = view_date if view_date is not None else today_in_zone(self._tz, now=now)
        # Stale pending release: background task (see `app.background.runner`).

        rows = self._rooms.list_rooms_with_desk_booking_for_date(day)
        order: list[uuid.UUID] = []
        grouped: dict[uuid.UUID, list[tuple[Desk, Booking | None]]] = {}
        room_by_id: dict[uuid.UUID, Room] = {}
        for room, desk, booking in rows:
            if room.id not in room_by_id:
                room_by_id[room.id] = room
                order.append(room.id)
                grouped[room.id] = []
            if desk is not None:
                grouped[room.id].append((desk, booking))

        result: list[RoomRead] = []
        for rid in order:
            room = room_by_id[rid]
            desk_pairs = sorted(
                grouped[rid],
                key=lambda t: (t[0].sort_order, t[0].name),
            )
            desks_out: list[DeskRead] = []
            for desk, booking in desk_pairs:
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

        today = today_in_zone(self._tz, now=now)
        if not is_booking_date_allowed(data.booking_date, today, max_ahead=5):
            msg = "booking_date is outside the allowed window"
            raise ValueError(msg)
        if data.booking_date == today and is_past_same_day_booking_cutoff(now, self._tz):
            msg = "same-day bookings are not available after 10:00"
            raise ValueError(msg)

        desk = self._rooms.get_desk(data.desk_id)
        if desk is None or not desk.bookable:
            msg = "desk is not bookable"
            raise ValueError(msg)

        existing = self._bookings.get_by_desk_and_date(data.desk_id, data.booking_date)
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
        self._bookings.add(booking)
        self._bookings.flush()
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

        booking = self._bookings.get_by_id(booking_id)
        if booking is None:
            msg = "booking not found"
            raise ValueError(msg)
        if booking.checked_in_at is not None:
            msg = "already checked in"
            raise ValueError(msg)
        if booking.display_name.strip() != display_name.strip():
            msg = "display name does not match"
            raise ValueError(msg)
        if booking.booking_date != today_in_zone(self._tz, now=now):
            msg = "check-in only on the booking day"
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
        self._bookings.flush()
        return BookingCreated(
            id=booking.id,
            desk_id=booking.desk_id,
            booking_date=booking.booking_date,
            display_name=booking.display_name,
        )
