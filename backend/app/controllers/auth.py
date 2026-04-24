from __future__ import annotations

from litestar import Controller, post
from sqlalchemy.orm import Session

from app.repositories.auth_repository import AuthRepository
from app.schema.auth import AuthTokenRequest, AuthTokenResponse
from app.services.auth_service import AuthService


class AuthController(Controller):
    path = "/auth"

    @post("/token", status_code=200, sync_to_thread=False)
    def request_token(
        self,
        data: AuthTokenRequest,
        session: Session,
        auth_service: AuthService,
    ) -> AuthTokenResponse:
        repo = AuthRepository(session)
        result = auth_service.authenticate(repo, data.password)
        return AuthTokenResponse.model_validate(result)
