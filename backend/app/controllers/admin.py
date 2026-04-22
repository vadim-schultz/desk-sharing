from __future__ import annotations

import uuid
from typing import ClassVar

from litestar import Controller, delete, get, patch, post
from litestar.types import Guard

from app.guards import require_admin_scope
from app.schema.admin import (
    AdminDeskCreate,
    AdminDeskRead,
    AdminDeskUpdate,
    AdminRoomCreate,
    AdminRoomRead,
    AdminRoomsListResponse,
    AdminRoomUpdate,
)
from app.services.admin_service import AdminService


class AdminRoomsController(Controller):
    path = "/admin/rooms"
    guards: ClassVar[list[Guard]] = [require_admin_scope]

    @get("/", sync_to_thread=False)
    def list_rooms(self, admin_service: AdminService) -> AdminRoomsListResponse:
        return admin_service.list_rooms()

    @get("/{room_id:uuid}", sync_to_thread=False)
    def get_room(self, room_id: uuid.UUID, admin_service: AdminService) -> AdminRoomRead:
        return admin_service.get_room(room_id)

    @post("/", status_code=201, sync_to_thread=False)
    def create_room(
        self, data: AdminRoomCreate, admin_service: AdminService
    ) -> AdminRoomRead:
        return admin_service.create_room(data)

    @patch("/{room_id:uuid}", sync_to_thread=False)
    def update_room(
        self,
        room_id: uuid.UUID,
        data: AdminRoomUpdate,
        admin_service: AdminService,
    ) -> AdminRoomRead:
        return admin_service.update_room(room_id, data)

    @delete("/{room_id:uuid}", status_code=204, sync_to_thread=False)
    def delete_room(self, room_id: uuid.UUID, admin_service: AdminService) -> None:
        admin_service.delete_room(room_id)

    @post("/{room_id:uuid}/desks", status_code=201, sync_to_thread=False)
    def create_desk(
        self,
        room_id: uuid.UUID,
        data: AdminDeskCreate,
        admin_service: AdminService,
    ) -> AdminDeskRead:
        return admin_service.create_desk(room_id, data)


class AdminDesksController(Controller):
    path = "/admin/desks"
    guards: ClassVar[list[Guard]] = [require_admin_scope]

    @patch("/{desk_id:uuid}", sync_to_thread=False)
    def update_desk(
        self,
        desk_id: uuid.UUID,
        data: AdminDeskUpdate,
        admin_service: AdminService,
    ) -> AdminDeskRead:
        return admin_service.update_desk(desk_id, data)

    @delete("/{desk_id:uuid}", status_code=204, sync_to_thread=False)
    def delete_desk(self, desk_id: uuid.UUID, admin_service: AdminService) -> None:
        admin_service.delete_desk(desk_id)
