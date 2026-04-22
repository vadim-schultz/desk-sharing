from __future__ import annotations

import uuid

from litestar.exceptions import NotFoundException
from sqlalchemy.orm import Session

from app.models import Desk, Room
from app.repositories import DeskRepository, RoomRepository
from app.rooms_txt import room_display_name
from app.schema.admin import (
    AdminDeskCreate,
    AdminDeskRead,
    AdminDeskUpdate,
    AdminRoomCreate,
    AdminRoomRead,
    AdminRoomsListResponse,
    AdminRoomUpdate,
)


class AdminService:
    def __init__(self, session: Session, rooms: RoomRepository, desks: DeskRepository) -> None:
        self._session = session
        self._rooms = rooms
        self._desks = desks

    def list_rooms(self) -> AdminRoomsListResponse:
        rows = self._rooms.find_all()
        return AdminRoomsListResponse(rooms=[self._room_read(r) for r in rows])

    def get_room(self, room_id: uuid.UUID) -> AdminRoomRead:
        room = self._rooms.get(room_id)
        if room is None:
            raise NotFoundException(detail="Room not found")
        return self._room_read(room)

    def create_room(self, data: AdminRoomCreate) -> AdminRoomRead:
        name = data.name or room_display_name(data.room_number, data.description)
        mx = self._rooms.max_sort_order()
        sort_order = (
            data.sort_order if data.sort_order is not None else (0 if mx is None else mx + 1)
        )
        room = Room(
            id=uuid.uuid4(),
            room_number=data.room_number.strip(),
            description=data.description.strip(),
            name=name.strip(),
            sort_order=sort_order,
        )
        self._rooms.add(room)
        self._session.flush()
        return self._room_read(room)

    def update_room(self, room_id: uuid.UUID, data: AdminRoomUpdate) -> AdminRoomRead:
        room = self._rooms.get(room_id)
        if room is None:
            raise NotFoundException(detail="Room not found")
        payload = data.model_dump(exclude_unset=True)
        if "room_number" in payload and payload["room_number"] is not None:
            room.room_number = str(payload["room_number"]).strip()
        if "description" in payload and payload["description"] is not None:
            room.description = str(payload["description"]).strip()
        if "name" in payload and payload["name"] is not None:
            room.name = str(payload["name"]).strip()
        if "sort_order" in payload and payload["sort_order"] is not None:
            room.sort_order = int(payload["sort_order"])
        self._session.flush()
        self._session.refresh(room)
        loaded = self._rooms.get(room_id)
        assert loaded is not None
        return self._room_read(loaded)

    def delete_room(self, room_id: uuid.UUID) -> None:
        room = self._rooms.get(room_id)
        if room is None:
            raise NotFoundException(detail="Room not found")
        self._rooms.delete(room)
        self._session.flush()

    def create_desk(self, room_id: uuid.UUID, data: AdminDeskCreate) -> AdminDeskRead:
        room = self._rooms.get(room_id)
        if room is None:
            raise NotFoundException(detail="Room not found")
        mx = self._desks.max_sort_order(room_id)
        sort_order = (
            data.sort_order if data.sort_order is not None else (0 if mx is None else mx + 1)
        )
        desk = Desk(
            id=uuid.uuid4(),
            room_id=room_id,
            name=data.name.strip(),
            bookable=data.bookable,
            monitor_count=data.monitor_count,
            has_keyboard=data.has_keyboard,
            has_mouse=data.has_mouse,
            sort_order=sort_order,
        )
        self._desks.add(desk)
        self._session.flush()
        return self._desk_read(desk)

    def update_desk(self, desk_id: uuid.UUID, data: AdminDeskUpdate) -> AdminDeskRead:
        desk = self._desks.get(desk_id)
        if desk is None:
            raise NotFoundException(detail="Desk not found")
        payload = data.model_dump(exclude_unset=True)
        if "name" in payload and payload["name"] is not None:
            desk.name = str(payload["name"]).strip()
        if "bookable" in payload and payload["bookable"] is not None:
            desk.bookable = bool(payload["bookable"])
        if "monitor_count" in payload and payload["monitor_count"] is not None:
            desk.monitor_count = int(payload["monitor_count"])
        if "has_keyboard" in payload and payload["has_keyboard"] is not None:
            desk.has_keyboard = bool(payload["has_keyboard"])
        if "has_mouse" in payload and payload["has_mouse"] is not None:
            desk.has_mouse = bool(payload["has_mouse"])
        if "sort_order" in payload and payload["sort_order"] is not None:
            desk.sort_order = int(payload["sort_order"])
        self._session.flush()
        self._session.refresh(desk)
        return self._desk_read(desk)

    def delete_desk(self, desk_id: uuid.UUID) -> None:
        desk = self._desks.get(desk_id)
        if desk is None:
            raise NotFoundException(detail="Desk not found")
        self._desks.delete(desk)
        self._session.flush()

    def _desk_read(self, desk: Desk) -> AdminDeskRead:
        return AdminDeskRead.model_validate(desk)

    def _room_read(self, room: Room) -> AdminRoomRead:
        desks = sorted(room.desks, key=lambda d: (d.sort_order, d.name))
        return AdminRoomRead(
            id=room.id,
            room_number=room.room_number,
            description=room.description,
            name=room.name,
            sort_order=room.sort_order,
            desks=[self._desk_read(d) for d in desks],
        )
