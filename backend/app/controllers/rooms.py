from datetime import date
from typing import Annotated

from litestar import Controller, get
from litestar.exceptions import HTTPException
from litestar.params import Parameter

from app.config import settings
from app.schema.booking import RoomsWithStatusResponse
from app.services.booking_service import BookingService


class RoomsController(Controller):
    path = "/rooms"

    @get("/", sync_to_thread=False)
    def list_rooms(
        self,
        booking_service: BookingService,
        booking_date: Annotated[
            date | None,
            Parameter(query="booking_date", required=False),
        ] = None,
    ) -> RoomsWithStatusResponse:
        try:
            day, rooms = booking_service.list_rooms_for_date(booking_date)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return RoomsWithStatusResponse(date=day, timezone=settings.app_timezone, rooms=rooms)
