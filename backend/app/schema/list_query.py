"""Pydantic models for repository list filters and sort (API ↔ SQL)."""

from __future__ import annotations

import uuid
from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


class RoomListFilter(BaseModel):
    """When ``booking_date`` is set, list uses room-desk-booking join for that day."""

    booking_date: date | None = None


class RoomListSort(BaseModel):
    sort_by: Literal["sort_order", "room_number", "name"] = "sort_order"
    sort_order: Literal["asc", "desc"] = "asc"


class RoomListQuery(BaseModel):
    filter: RoomListFilter = Field(default_factory=RoomListFilter)
    sort: RoomListSort = Field(default_factory=RoomListSort)


class DeskListFilter(BaseModel):
    room_id: uuid.UUID


class DeskListSort(BaseModel):
    sort_by: Literal["sort_order", "name"] = "sort_order"
    sort_order: Literal["asc", "desc"] = "asc"


class DeskListQuery(BaseModel):
    filter: DeskListFilter
    sort: DeskListSort = Field(default_factory=DeskListSort)
