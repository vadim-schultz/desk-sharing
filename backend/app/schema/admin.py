from __future__ import annotations

import uuid
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field


def _strip_str(v: object) -> object:
    if isinstance(v, str):
        return v.strip()
    return v


def _strip_optional_str(v: object) -> object:
    if v is None:
        return None
    if isinstance(v, str):
        return v.strip()
    return v


StrippedStr = Annotated[str, BeforeValidator(_strip_str)]
StrippedOptionalStr = Annotated[str | None, BeforeValidator(_strip_optional_str)]


class AdminDeskRead(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    name: str = Field(..., min_length=1, max_length=200)
    bookable: bool
    monitor_count: int = Field(..., ge=0)
    has_keyboard: bool
    has_mouse: bool
    sort_order: int


class AdminRoomRead(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    room_number: str = Field(..., min_length=1, max_length=64)
    description: str = Field(default="", max_length=500)
    name: str = Field(..., min_length=1, max_length=600)
    sort_order: int
    desks: list[AdminDeskRead]


class AdminRoomsListResponse(BaseModel):
    rooms: list[AdminRoomRead]


class AdminRoomCreate(BaseModel):
    room_number: StrippedStr = Field(..., min_length=1, max_length=64)
    description: StrippedStr = Field(default="", max_length=500)
    name: StrippedOptionalStr = Field(default=None, min_length=1, max_length=600)
    sort_order: int | None = None


class AdminRoomUpdate(BaseModel):
    room_number: StrippedOptionalStr = Field(default=None, min_length=1, max_length=64)
    description: StrippedOptionalStr = Field(default=None, max_length=500)
    name: StrippedOptionalStr = Field(default=None, min_length=1, max_length=600)
    sort_order: int | None = None


class AdminDeskCreate(BaseModel):
    room_id: uuid.UUID
    name: StrippedStr = Field(..., min_length=1, max_length=200)
    bookable: bool = True
    monitor_count: int = Field(default=0, ge=0)
    has_keyboard: bool = False
    has_mouse: bool = False
    sort_order: int | None = None


class AdminDeskUpdate(BaseModel):
    name: StrippedOptionalStr = Field(default=None, min_length=1, max_length=200)
    bookable: bool | None = None
    monitor_count: int | None = Field(default=None, ge=0)
    has_keyboard: bool | None = None
    has_mouse: bool | None = None
    sort_order: int | None = None
