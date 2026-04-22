from __future__ import annotations

from importlib import import_module

import uvicorn
from litestar import Litestar

from app.background.runner import start_maintenance_thread, stop_maintenance_thread
from app.controllers import BookingsController, RoomsController, health_check
from app.dependencies import dependencies
from app.middleware.cors import cors_config


def create_app() -> Litestar:
    import_module("app.background.callbacks")
    return Litestar(
        route_handlers=[RoomsController, BookingsController, health_check],
        dependencies=dependencies,
        cors_config=cors_config,
        on_startup=[start_maintenance_thread],
        on_shutdown=[stop_maintenance_thread],
    )


app = create_app()


def run() -> None:
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
