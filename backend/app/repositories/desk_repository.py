from __future__ import annotations

import uuid

from sqlalchemy import ColumnElement, func, select
from sqlalchemy.orm import Session

from app.models import Desk
from app.schema.list_query import DeskListQuery, DeskListSort


def _desk_primary_order(sort: DeskListSort) -> ColumnElement:
    col = getattr(Desk, sort.sort_by)
    return col.asc() if sort.sort_order == "asc" else col.desc()


class DeskRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list(self, query: DeskListQuery) -> list[Desk]:
        stmt = (
            select(Desk)
            .where(Desk.room_id == query.filter.room_id)
            .order_by(
                _desk_primary_order(query.sort),
                Desk.sort_order.asc(),
                Desk.name.asc(),
            )
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
