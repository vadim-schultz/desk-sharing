"""Dependency injection: DB session, repositories-backed services."""

from __future__ import annotations

from typing import Any

from litestar.di import Provide
from sqlalchemy.orm import Session

from app.db import provide_session
from app.repositories import BookingRepository, DeskRepository, RoomRepository
from app.services.admin_service import AdminService
from app.services.auth_service import auth_service_singleton
from app.services.booking_service import BookingService


def create_booking_service(session: Session) -> BookingService:
    return BookingService(
        RoomRepository(session),
        BookingRepository(session),
        DeskRepository(session),
    )


def provide_booking_service(session: Session) -> BookingService:
    return create_booking_service(session)


def provide_admin_service(session: Session) -> AdminService:
    return AdminService(
        session,
        RoomRepository(session),
        DeskRepository(session),
    )


dependencies: dict[str, Any] = {
    "session": Provide(provide_session),
    "booking_service": Provide(provide_booking_service, sync_to_thread=False),
    "auth_service": Provide(lambda: auth_service_singleton, sync_to_thread=False),
    "admin_service": Provide(provide_admin_service, sync_to_thread=False),
}
