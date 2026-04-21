"""Insert rooms from `rooms.txt` and four desks per room."""

from __future__ import annotations

import uuid

from app.db import SessionLocal, engine
from app.models import Desk, Room
from app.rooms_txt import default_rooms_txt_path, parse_rooms_file, room_display_name
from sqlalchemy import select
from sqlalchemy.orm import Session


def seed(session: Session) -> None:
    rows = parse_rooms_file(default_rooms_txt_path())
    if not rows:
        msg = "no rooms parsed from rooms.txt"
        raise ValueError(msg)

    rooms: list[Room] = []
    for sort_order, (room_number, description) in enumerate(rows):
        name = room_display_name(room_number, description)
        rooms.append(
            Room(
                id=uuid.uuid4(),
                room_number=room_number,
                description=description,
                name=name,
                sort_order=sort_order,
            )
        )
    session.add_all(rooms)
    session.flush()

    desks: list[Desk] = []
    for room in rooms:
        for i in range(4):
            desks.append(
                Desk(
                    id=uuid.uuid4(),
                    room_id=room.id,
                    name=f"Desk {i + 1}",
                    bookable=True,
                    monitor_count=1,
                    has_keyboard=True,
                    has_mouse=True,
                    sort_order=i,
                )
            )
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
