from __future__ import annotations

import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Desk


class DeskRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list(self, room_id: uuid.UUID) -> list[Desk]:
        stmt = (
            select(Desk)
            .where(Desk.room_id == room_id)
            .order_by(Desk.sort_order, Desk.name)
        )
        return list(self._session.scalars(stmt))

    def get(self, desk_id: uuid.UUID) -> Desk | None:
        return self._session.get(Desk, desk_id)

    def add(self, desk: Desk) -> None:
        self._session.add(desk)

    def delete(self, desk: Desk) -> None:
        self._session.delete(desk)

    def max_sort_order(self, room_id: uuid.UUID) -> int | None:
        return self._session.scalar(
            select(func.max(Desk.sort_order)).where(Desk.room_id == room_id)
        )

    def count(self, room_id: uuid.UUID) -> int:
        n = self._session.scalar(
            select(func.count()).select_from(Desk).where(Desk.room_id == room_id)
        )
        return int(n or 0)
