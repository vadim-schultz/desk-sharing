from __future__ import annotations

from sqlalchemy.orm import Session

from app.background.registry import register_callback
from app.services.maintenance import release_stale_pending_bookings


def _release_stale_pending(session: Session) -> None:
    release_stale_pending_bookings(session)


def register_default_callbacks() -> None:
    register_callback(_release_stale_pending)


# Register on import; additional callbacks can be registered the same way from other modules
register_default_callbacks()
