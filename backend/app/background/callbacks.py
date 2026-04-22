from __future__ import annotations

from sqlalchemy.orm import Session

from app.background.registry import register_callback


def _release_stale_pending(session: Session) -> None:
    from app.dependencies import create_booking_service

    create_booking_service(session).release_stale_pending()


def register_default_callbacks() -> None:
    register_callback(_release_stale_pending)


# Register on import; additional callbacks can be registered the same way from other modules
register_default_callbacks()
