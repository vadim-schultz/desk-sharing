from __future__ import annotations

import uuid
from datetime import date

from pydantic import BaseModel, Field

from app.schema.room import RoomRead


class BookingCreate(BaseModel):
    desk_id: uuid.UUID
    booking_date: date
    display_name: str = Field(..., min_length=1, max_length=200)


class BookingCreated(BaseModel):
    id: uuid.UUID
    desk_id: uuid.UUID
    booking_date: date
    display_name: str


class CheckInRequest(BaseModel):
    display_name: str = Field(..., min_length=1, max_length=200)


class RoomsWithStatusResponse(BaseModel):
    date: date
    timezone: str
    rooms: list[RoomRead]
