from __future__ import annotations

import os

os.environ.setdefault("DATABASE_URL", "postgresql+psycopg://desk:desk@localhost:5432/desk")
os.environ["MAINTENANCE_TASK_ENABLED"] = "false"

import pytest
from app.db import engine
from app.main import create_app
from app.models import Base
from litestar import Litestar
from litestar.testing import TestClient


@pytest.fixture(autouse=True)
def reset_db() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


@pytest.fixture
def app() -> Litestar:
    return create_app()


@pytest.fixture
def client(app: Litestar) -> TestClient[Litestar]:
    return TestClient(app)
