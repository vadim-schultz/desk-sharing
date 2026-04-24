from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING, Literal

from sqlalchemy import Date, DateTime, ForeignKey, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.desk import Desk


class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (UniqueConstraint("desk_id", "booking_date", name="uq_booking_desk_date"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    desk_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("desks.id", ondelete="CASCADE"), nullable=False
    )
    booking_date: Mapped[date] = mapped_column(Date, nullable=False)
    display_name: Mapped[str] = mapped_column(String(200), nullable=False)
    checked_in_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    desk: Mapped[Desk] = relationship("Desk", back_populates="bookings")

    def has_reservation_for_day(self) -> Literal[True]:
        return True
