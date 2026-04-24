from __future__ import annotations

import uuid
from collections import defaultdict

from litestar.exceptions import NotFoundException
from sqlalchemy.orm import Session

from app.models import Room
from app.repositories import RoomRepository
from app.rooms_txt import room_display_name
from app.schema.admin import (
    AdminDeskRead,
    AdminRoomCreate,
    AdminRoomRead,
    AdminRoomsListResponse,
    AdminRoomUpdate,
)
from app.schema.list_query import RoomListQuery


def to_admin_room_read(room: Room) -> AdminRoomRead:
    return AdminRoomRead(
        id=room.id,
        room_number=room.room_number,
        description=room.description,
        name=room.name,
        sort_order=room.sort_order,
        desks=[AdminDeskRead.model_validate(d) for d in room.desks],
    )


class RoomAdminService:
    def __init__(self, session: Session, rooms: RoomRepository) -> None:
        self._session = session
        self._rooms = rooms

    def list(self, query: RoomListQuery) -> AdminRoomsListResponse:
        if query.filter.booking_date is not None:
            msg = "admin room list must not set booking_date on filter"
            raise ValueError(msg)
        rows = self._rooms.list_rooms(query)
        order: list[uuid.UUID] = []
        room_by_id: dict[uuid.UUID, Room] = {}
        desks_by_room: dict[uuid.UUID, list[AdminDeskRead]] = defaultdict(list)
        for row in rows:
            rid = row.room.id
            if rid not in room_by_id:
                room_by_id[rid] = row.room
                order.append(rid)
            if row.desk.participates_in_layout():
                desk_read = row.desk.to_admin_desk_read()
                if desk_read is not None:
                    desks_by_room[rid].append(desk_read)
        rooms_out = [
            AdminRoomRead(
                id=room_by_id[rid].id,
                room_number=room_by_id[rid].room_number,
                description=room_by_id[rid].description,
                name=room_by_id[rid].name,
                sort_order=room_by_id[rid].sort_order,
                desks=desks_by_room[rid],
            )
            for rid in order
        ]
        return AdminRoomsListResponse(rooms=rooms_out)

    def get(self, room_id: uuid.UUID) -> AdminRoomRead:
        room = self._rooms.get(room_id)
        if room is None:
            raise NotFoundException(detail="Room not found")
        return to_admin_room_read(room)

    def create(self, data: AdminRoomCreate) -> AdminRoomRead:
        name = data.name or room_display_name(data.room_number, data.description)
        mx = self._rooms.max_sort_order()
        sort_order = (
            data.sort_order if data.sort_order is not None else (0 if mx is None else mx + 1)
        )
        room = Room(
            id=uuid.uuid4(),
            room_number=data.room_number,
            description=data.description,
            name=name,
            sort_order=sort_order,
        )
        self._rooms.add(room)
        self._session.flush()
        return to_admin_room_read(room)

    def update(self, room_id: uuid.UUID, data: AdminRoomUpdate) -> AdminRoomRead:
        room = self._rooms.get(room_id)
        if room is None:
            raise NotFoundException(detail="Room not found")
        for k, v in data.model_dump(exclude_unset=True, exclude_none=True).items():
            setattr(room, k, v)
        self._session.flush()
        self._session.refresh(room)
        loaded = self._rooms.get(room_id)
        assert loaded is not None
        return to_admin_room_read(loaded)

    def delete(self, room_id: uuid.UUID) -> None:
        room = self._rooms.get(room_id)
        if room is None:
            raise NotFoundException(detail="Room not found")
        self._rooms.delete(room)
        self._session.flush()
