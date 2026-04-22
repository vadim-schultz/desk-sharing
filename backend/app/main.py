from __future__ import annotations

from importlib import import_module

import uvicorn
from litestar import Litestar

from app.background.runner import start_maintenance_thread, stop_maintenance_thread
from app.controllers import (
    AdminDesksController,
    AdminRoomsController,
    AuthController,
    BookingsController,
    RoomsController,
    health_check,
)
from app.dependencies import dependencies
from app.middleware.cors import cors_config
from app.services.auth_service import auth_service_singleton


def create_app() -> Litestar:
    import_module("app.background.callbacks")
    app = Litestar(
        route_handlers=[
            AuthController,
            RoomsController,
            BookingsController,
            AdminRoomsController,
            AdminDesksController,
            health_check,
        ],
        dependencies=dependencies,
        cors_config=cors_config,
        on_startup=[start_maintenance_thread],
        on_shutdown=[stop_maintenance_thread],
    )
    # Guards read ``app.state``; set synchronously so ``TestClient`` works without lifespan.
    app.state.auth_service = auth_service_singleton
    return app


app = create_app()


def run() -> None:
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
