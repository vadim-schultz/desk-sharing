from __future__ import annotations

from pydantic import BaseModel, Field


class AuthTokenRequest(BaseModel):
    password: str = Field(..., min_length=1)


class AuthTokenResponse(BaseModel):
    access_token: str
    expires_in: int
