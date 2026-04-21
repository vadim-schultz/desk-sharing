from __future__ import annotations

import uuid

from litestar import Controller, post
from litestar.exceptions import HTTPException

from app.schema.booking import BookingCreate, BookingCreated, CheckInRequest
from app.services.booking_service import BookingService


class BookingsController(Controller):
    path = "/bookings"

    @post("/", status_code=201, sync_to_thread=False)
    def create(self, data: BookingCreate, booking_service: BookingService) -> BookingCreated:
        try:
            return booking_service.create_booking(data)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @post("/{booking_id:uuid}/check-in", status_code=201, sync_to_thread=False)
    def check_in(
        self,
        booking_id: uuid.UUID,
        data: CheckInRequest,
        booking_service: BookingService,
    ) -> BookingCreated:
        try:
            return booking_service.check_in(booking_id, data.display_name)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
