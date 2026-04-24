from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import cast

from app.config import settings
from app.models import Booking, Desk, Room
from app.repositories import RoomRepository
from app.schema.desk import DeskRead
from app.schema.enums import DeskDayStatus
from app.schema.list_query import RoomListFilter, RoomListQuery
from app.schema.room import RoomRead
from app.timeutil import get_zone, today_in_zone


class RoomCatalogService:
    def __init__(self, room_repo: RoomRepository) -> None:
        self._rooms = room_repo
        self._tz = get_zone(settings.app_timezone)

    def list(
        self,
        query: RoomListQuery,
        now: datetime | None = None,
    ) -> tuple[date, list[RoomRead]]:
        if now is None:
            now = datetime.now(tz=self._tz)
        elif now.tzinfo is None:
            msg = "now must be timezone-aware"
            raise ValueError(msg)

        day = (
            query.filter.booking_date
            if query.filter.booking_date is not None
            else today_in_zone(self._tz, now=now)
        )
        list_query = RoomListQuery(
            filter=RoomListFilter(booking_date=day),
            sort=query.sort,
        )
        rows = cast(
            "list[tuple[Room, Desk | None, Booking | None]]",
            self._rooms.list_rooms(list_query),
        )

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
            desk_pairs = grouped[rid]
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
