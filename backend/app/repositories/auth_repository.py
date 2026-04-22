from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.admin_credential import ADMIN_PASSWORD_KEY, AdminCredential


class AuthRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_password_hash(self) -> str | None:
        row = self._session.get(AdminCredential, ADMIN_PASSWORD_KEY)
        return row.password_hash if row is not None else None

    def set_password_hash(self, hashed: str) -> None:
        row = self._session.get(AdminCredential, ADMIN_PASSWORD_KEY)
        if row is None:
            self._session.add(AdminCredential(key=ADMIN_PASSWORD_KEY, password_hash=hashed))
        else:
            row.password_hash = hashed
