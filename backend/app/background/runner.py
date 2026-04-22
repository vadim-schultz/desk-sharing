from __future__ import annotations

import logging
import threading

import litestar

from app.background.registry import run_all_maintenance
from app.config import settings
from app.db import SessionLocal

logger = logging.getLogger(__name__)


class _M:
    def __init__(self) -> None:
        self.thread: threading.Thread | None = None
        self.stop: threading.Event | None = None


_m = _M()


def _one_cycle() -> None:
    session = SessionLocal()
    try:
        run_all_maintenance(session)
        session.commit()
    except Exception:
        session.rollback()
        logger.exception("maintenance cycle failed")
    finally:
        session.close()


def _thread_main(stop: threading.Event) -> None:
    while not stop.is_set():
        _one_cycle()
        if stop.wait(timeout=settings.maintenance_interval_seconds):
            return


def start_maintenance_thread(app: litestar.Litestar) -> None:  # noqa: ARG001
    if not settings.maintenance_task_enabled or settings.maintenance_interval_seconds <= 0:
        return
    if _m.thread is not None and _m.thread.is_alive():
        return
    _m.stop = threading.Event()
    _m.thread = threading.Thread(
        name="maintenance",
        target=_thread_main,
        args=(_m.stop,),
        daemon=True,
    )
    _m.thread.start()


def stop_maintenance_thread() -> None:
    if _m.stop is not None:
        _m.stop.set()
    if _m.thread is not None and _m.thread.is_alive():
        _m.thread.join(timeout=5.0)
    _m.stop = None
    _m.thread = None
