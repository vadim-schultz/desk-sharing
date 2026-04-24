from __future__ import annotations

import uuid

from litestar.exceptions import NotFoundException
from sqlalchemy.orm import Session

from app.models import Desk
from app.repositories import DeskRepository, RoomRepository
from app.schema.admin import AdminDeskCreate, AdminDeskRead, AdminDeskUpdate


class DeskAdminService:
    def __init__(
        self,
        session: Session,
        desks: DeskRepository,
        rooms: RoomRepository,
    ) -> None:
        self._session = session
        self._desks = desks
        self._rooms = rooms

    def create(self, data: AdminDeskCreate) -> AdminDeskRead:
        room = self._rooms.get(data.room_id)
        if room is None:
            raise NotFoundException(detail="Room not found")
        mx = self._desks.max_sort_order(data.room_id)
        sort_order = (
            data.sort_order if data.sort_order is not None else (0 if mx is None else mx + 1)
        )
        desk = Desk(
            id=uuid.uuid4(),
            room_id=data.room_id,
            name=data.name,
            bookable=data.bookable,
            monitor_count=data.monitor_count,
            has_keyboard=data.has_keyboard,
            has_mouse=data.has_mouse,
            sort_order=sort_order,
        )
        self._desks.add(desk)
        self._session.flush()
        return AdminDeskRead.model_validate(desk)

    def update(self, desk_id: uuid.UUID, data: AdminDeskUpdate) -> AdminDeskRead:
        desk = self._desks.get(desk_id)
        if desk is None:
            raise NotFoundException(detail="Desk not found")
        for k, v in data.model_dump(exclude_unset=True, exclude_none=True).items():
            setattr(desk, k, v)
        self._session.flush()
        self._session.refresh(desk)
        return AdminDeskRead.model_validate(desk)

    def delete(self, desk_id: uuid.UUID) -> None:
        desk = self._desks.get(desk_id)
        if desk is None:
            raise NotFoundException(detail="Desk not found")
        self._desks.delete(desk)
        self._session.flush()
