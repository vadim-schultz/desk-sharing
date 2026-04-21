from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.booking import Booking
    from app.models.room import Room


class Desk(Base):
    __tablename__ = "desks"
    __table_args__ = (UniqueConstraint("room_id", "name", name="uq_desks_room_name"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    bookable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    monitor_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    has_keyboard: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    has_mouse: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    room: Mapped[Room] = relationship("Room", back_populates="desks")
    bookings: Mapped[list[Booking]] = relationship("Booking", back_populates="desk")
