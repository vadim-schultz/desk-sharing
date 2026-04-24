"""Dependency injection: DB session, repositories-backed services."""

from __future__ import annotations

from typing import Any

from litestar.di import Provide
from sqlalchemy.orm import Session

from app.db import provide_session
from app.repositories import BookingRepository, DeskRepository, RoomRepository
from app.services.auth_service import auth_service_singleton
from app.services.booking_service import BookingService
from app.services.desk_admin_service import DeskAdminService
from app.services.room_admin_service import RoomAdminService
from app.services.room_catalog_service import RoomCatalogService


def create_booking_service(session: Session) -> BookingService:
    return BookingService(
        BookingRepository(session),
        DeskRepository(session),
    )


def provide_booking_service(session: Session) -> BookingService:
    return create_booking_service(session)


def provide_room_catalog_service(session: Session) -> RoomCatalogService:
    return RoomCatalogService(RoomRepository(session))


def provide_room_admin_service(session: Session) -> RoomAdminService:
    return RoomAdminService(session, RoomRepository(session))


def provide_desk_admin_service(session: Session) -> DeskAdminService:
    return DeskAdminService(
        session,
        DeskRepository(session),
        RoomRepository(session),
    )


dependencies: dict[str, Any] = {
    "session": Provide(provide_session),
    "booking_service": Provide(provide_booking_service, sync_to_thread=False),
    "room_catalog_service": Provide(provide_room_catalog_service, sync_to_thread=False),
    "auth_service": Provide(lambda: auth_service_singleton, sync_to_thread=False),
    "room_admin_service": Provide(provide_room_admin_service, sync_to_thread=False),
    "desk_admin_service": Provide(provide_desk_admin_service, sync_to_thread=False),
}
