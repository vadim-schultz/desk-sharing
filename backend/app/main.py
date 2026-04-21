from __future__ import annotations

import uvicorn
from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.di import Provide
from sqlalchemy.orm import Session

from app.controllers import BookingsController, RoomsController, health_check
from app.db import provide_session
from app.services.booking_service import BookingService


def provide_booking_service(session: Session) -> BookingService:
    return BookingService(session)


def create_app() -> Litestar:
    return Litestar(
        route_handlers=[RoomsController, BookingsController, health_check],
        dependencies={
            "session": Provide(provide_session),
            "booking_service": Provide(provide_booking_service, sync_to_thread=False),
        },
        cors_config=CORSConfig(
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        ),
    )


app = create_app()


def run() -> None:
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
