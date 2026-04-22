from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

ADMIN_PASSWORD_KEY = "admin_password"


class AdminCredential(Base):
    """Single logical row for bcrypt-hashed admin password (see seed)."""

    __tablename__ = "admin_credentials"

    key: Mapped[str] = mapped_column(String(64), primary_key=True)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
