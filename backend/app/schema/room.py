from __future__ import annotations

import uuid

from pydantic import BaseModel, ConfigDict, Field

from app.schema.desk import DeskRead


class RoomRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str = Field(..., min_length=1, max_length=200)
    desks: list[DeskRead]
