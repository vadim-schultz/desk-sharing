from __future__ import annotations

import uuid

from pydantic import BaseModel, ConfigDict, Field

from app.schema.enums import DeskDayStatus


class DeskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str = Field(..., min_length=1, max_length=200)
    bookable: bool
    monitor_count: int = Field(..., ge=0)
    has_keyboard: bool
    has_mouse: bool
    status: DeskDayStatus
    booking_id: uuid.UUID | None = None
