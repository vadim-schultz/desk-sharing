from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.desk import Desk


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_number: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    name: Mapped[str] = mapped_column(String(600), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    desks: Mapped[list[Desk]] = relationship(
        "Desk", back_populates="room", cascade="all, delete-orphan", order_by="Desk.sort_order"
    )
