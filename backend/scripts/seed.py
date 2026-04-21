"""Insert demo rooms and desks."""

from __future__ import annotations

import uuid

from app.db import SessionLocal, engine
from app.models import Desk, Room
from sqlalchemy import select
from sqlalchemy.orm import Session


def seed(session: Session) -> None:
    r1 = Room(id=uuid.uuid4(), name="Quiet zone", sort_order=0)
    r2 = Room(id=uuid.uuid4(), name="Collaboration", sort_order=1)
    session.add_all([r1, r2])
    session.flush()

    desks = [
        Desk(
            id=uuid.uuid4(),
            room_id=r1.id,
            name="Desk A",
            bookable=True,
            monitor_count=2,
            has_keyboard=True,
            has_mouse=True,
            sort_order=0,
        ),
        Desk(
            id=uuid.uuid4(),
            room_id=r1.id,
            name="Desk B",
            bookable=True,
            monitor_count=1,
            has_keyboard=True,
            has_mouse=False,
            sort_order=1,
        ),
        Desk(
            id=uuid.uuid4(),
            room_id=r2.id,
            name="Hot desk 1",
            bookable=False,
            monitor_count=0,
            has_keyboard=False,
            has_mouse=False,
            sort_order=0,
        ),
    ]
    session.add_all(desks)


def main() -> None:
    with SessionLocal() as session:
        if session.scalar(select(Room.id).limit(1)) is not None:
            return
        seed(session)
        session.commit()
    engine.dispose()


if __name__ == "__main__":
    main()
