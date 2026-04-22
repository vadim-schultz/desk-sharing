"""Dependency injection: DB session, repositories-backed services."""

from __future__ import annotations

from typing import Any

from litestar.di import Provide
from sqlalchemy.orm import Session

from app.db import provide_session
from app.repositories import BookingRepository, RoomRepository
from app.services.booking_service import BookingService


def create_booking_service(session: Session) -> BookingService:
    return BookingService(
        RoomRepository(session),
        BookingRepository(session),
    )


def provide_booking_service(session: Session) -> BookingService:
    return create_booking_service(session)


dependencies: dict[str, Any] = {
    "session": Provide(provide_session),
    "booking_service": Provide(provide_booking_service, sync_to_thread=False),
}
