from __future__ import annotations

import os
import uuid

os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
os.environ["MAINTENANCE_TASK_ENABLED"] = "false"

import pytest
from app.db import SessionLocal, engine
from app.main import create_app
from app.models import Base, Desk, Room
from app.seed_admin import ensure_admin_password
from litestar import Litestar
from litestar.testing import TestClient


@pytest.fixture(autouse=True)
def reset_db() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with SessionLocal() as session:
        ensure_admin_password(session)
        session.commit()


@pytest.fixture
def room_desk() -> tuple[uuid.UUID, uuid.UUID]:
    with SessionLocal() as session:
        room = Room(
            id=uuid.uuid4(),
            room_number="T-1",
            description="Test room",
            name="T-1 - Test room",
            sort_order=0,
        )
        session.add(room)
        session.flush()
        desk = Desk(
            id=uuid.uuid4(),
            room_id=room.id,
            name="Desk 1",
            bookable=True,
            monitor_count=1,
            has_keyboard=True,
            has_mouse=True,
            sort_order=0,
        )
        session.add(desk)
        session.commit()
        return room.id, desk.id


@pytest.fixture
def app() -> Litestar:
    return create_app()


@pytest.fixture
def client(app: Litestar) -> TestClient[Litestar]:
    return TestClient(app)
