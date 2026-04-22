from __future__ import annotations

from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.handlers import BaseRouteHandler

_BEARER_PREFIX = "Bearer "


def require_admin_scope(connection: ASGIConnection, _: BaseRouteHandler) -> None:
    """Reject requests without valid ``Authorization: Bearer`` admin JWT."""
    auth_header = connection.headers.get("authorization", "")
    if not auth_header.lower().startswith(_BEARER_PREFIX.lower()):
        raise NotAuthorizedException(detail="Missing authorization token")

    token = auth_header[len(_BEARER_PREFIX) :].strip()
    if not token:
        raise NotAuthorizedException(detail="Missing authorization token")

    auth_service = connection.app.state.auth_service
    auth_service.verify_token(token)
