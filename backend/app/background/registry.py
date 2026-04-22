from __future__ import annotations

from collections.abc import Callable

from sqlalchemy.orm import Session

MaintenanceCallback = Callable[[Session], None]

_callbacks: list[MaintenanceCallback] = []


def register_callback(callback: MaintenanceCallback) -> None:
    if callback not in _callbacks:
        _callbacks.append(callback)


def get_callbacks() -> list[MaintenanceCallback]:
    return list(_callbacks)


def run_all_maintenance(session: Session) -> None:
    for cb in _callbacks:
        cb(session)
