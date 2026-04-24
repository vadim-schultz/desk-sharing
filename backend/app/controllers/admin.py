from __future__ import annotations

import uuid
from typing import Annotated, ClassVar, Literal

from litestar import Controller, delete, get, patch, post
from litestar.params import Parameter
from litestar.status_codes import HTTP_201_CREATED, HTTP_204_NO_CONTENT
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
from app.schema.list_query import RoomListFilter, RoomListQuery, RoomListSort
from app.services.desk_admin_service import DeskAdminService
from app.services.room_admin_service import RoomAdminService


class AdminRoomsController(Controller):
    path = "/admin/rooms"
    guards: ClassVar[tuple[Guard, ...]] = (require_admin_scope,)

    @get("/", sync_to_thread=False)
    def list(
        self,
        room_admin_service: RoomAdminService,
        sort_by: Annotated[
            Literal["sort_order", "room_number", "name"],
            Parameter(query="sort_by", required=False),
        ] = "sort_order",
        sort_dir: Annotated[
            Literal["asc", "desc"],
            Parameter(query="sort_dir", required=False),
        ] = "asc",
    ) -> AdminRoomsListResponse:
        q = RoomListQuery(
            filter=RoomListFilter(),
            sort=RoomListSort(sort_by=sort_by, sort_order=sort_dir),
        )
        return room_admin_service.list(q)

    @get("/{room_id:uuid}", sync_to_thread=False)
    def get(self, room_id: uuid.UUID, room_admin_service: RoomAdminService) -> AdminRoomRead:
        return room_admin_service.get(room_id)

    @post("/", status_code=HTTP_201_CREATED, sync_to_thread=False)
    def create(self, data: AdminRoomCreate, room_admin_service: RoomAdminService) -> AdminRoomRead:
        return room_admin_service.create(data)

    @patch("/{room_id:uuid}", sync_to_thread=False)
    def update(
        self,
        room_id: uuid.UUID,
        data: AdminRoomUpdate,
        room_admin_service: RoomAdminService,
    ) -> AdminRoomRead:
        return room_admin_service.update(room_id, data)

    @delete("/{room_id:uuid}", status_code=HTTP_204_NO_CONTENT, sync_to_thread=False)
    def delete(self, room_id: uuid.UUID, room_admin_service: RoomAdminService) -> None:
        room_admin_service.delete(room_id)


class AdminDesksController(Controller):
    path = "/admin/desks"
    guards: ClassVar[tuple[Guard, ...]] = (require_admin_scope,)

    @post("/", status_code=HTTP_201_CREATED, sync_to_thread=False)
    def create(self, data: AdminDeskCreate, desk_admin_service: DeskAdminService) -> AdminDeskRead:
        return desk_admin_service.create(data)

    @patch("/{desk_id:uuid}", sync_to_thread=False)
    def update(
        self,
        desk_id: uuid.UUID,
        data: AdminDeskUpdate,
        desk_admin_service: DeskAdminService,
    ) -> AdminDeskRead:
        return desk_admin_service.update(desk_id, data)

    @delete("/{desk_id:uuid}", status_code=HTTP_204_NO_CONTENT, sync_to_thread=False)
    def delete(self, desk_id: uuid.UUID, desk_admin_service: DeskAdminService) -> None:
        desk_admin_service.delete(desk_id)
