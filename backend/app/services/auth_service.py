from __future__ import annotations

from datetime import UTC, datetime, timedelta

import bcrypt
import jwt
from litestar.exceptions import NotAuthorizedException

from app.config import Settings, settings
from app.repositories.auth_repository import AuthRepository

JWT_SCOPE_ADMIN = "admin"


class AuthService:
    """Password verification and JWT issue/verify for admin scope."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def authenticate(self, repo: AuthRepository, password: str) -> dict[str, str | int]:
        stored = repo.get_password_hash()
        if stored is None:
            raise NotAuthorizedException(detail="Auth not configured")

        if not bcrypt.checkpw(password.encode("utf-8"), stored.encode("utf-8")):
            raise NotAuthorizedException(detail="Invalid password")

        expires_delta = timedelta(minutes=self._settings.jwt_expiry_minutes)
        now = datetime.now(UTC)
        payload = {
            "exp": now + expires_delta,
            "iat": now,
            "scope": JWT_SCOPE_ADMIN,
        }
        token = jwt.encode(
            payload,
            self._settings.jwt_secret,
            algorithm=self._settings.jwt_algorithm,
        )
        return {
            "access_token": token,
            "expires_in": int(expires_delta.total_seconds()),
        }

    def verify_token(self, token: str) -> dict[str, object]:
        try:
            payload = jwt.decode(
                token,
                self._settings.jwt_secret,
                algorithms=[self._settings.jwt_algorithm],
            )
        except jwt.ExpiredSignatureError:
            raise NotAuthorizedException(detail="Token expired") from None
        except jwt.InvalidTokenError as exc:
            raise NotAuthorizedException(detail="Invalid token") from exc

        if payload.get("scope") != JWT_SCOPE_ADMIN:
            raise NotAuthorizedException(detail="Insufficient scope")
        return payload


auth_service_singleton = AuthService(settings)
