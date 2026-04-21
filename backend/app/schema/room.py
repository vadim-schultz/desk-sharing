from __future__ import annotations

import uuid

from pydantic import BaseModel, ConfigDict, Field

from app.schema.desk import DeskRead


class RoomRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    room_number: str = Field(..., min_length=1, max_length=64)
    description: str = Field(default="", max_length=500)
    name: str = Field(..., min_length=1, max_length=600)
    desks: list[DeskRead]
