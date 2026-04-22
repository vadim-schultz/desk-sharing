"""Upsert default admin password (plaintext ``dresden``) as bcrypt hash."""

from __future__ import annotations

import bcrypt
from sqlalchemy.orm import Session

from app.models.admin_credential import ADMIN_PASSWORD_KEY, AdminCredential


def hash_default_admin_password() -> str:
    return bcrypt.hashpw(b"dresden", bcrypt.gensalt()).decode()


def ensure_admin_password(session: Session) -> None:
    """Ensure the admin row exists and matches the default dev password."""
    hashed = hash_default_admin_password()
    row = session.get(AdminCredential, ADMIN_PASSWORD_KEY)
    if row is None:
        session.add(AdminCredential(key=ADMIN_PASSWORD_KEY, password_hash=hashed))
    else:
        row.password_hash = hashed
