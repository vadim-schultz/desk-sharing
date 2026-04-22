from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://desk:desk@localhost:5432/desk"
    app_timezone: str = "Europe/Berlin"
    jwt_secret: str = Field(
        default="dev-only-jwt-secret-change-in-production",
        description="HS256 signing key for admin JWTs.",
    )
    jwt_algorithm: str = Field(default="HS256")
    jwt_expiry_minutes: int = Field(default=60, ge=1, le=24 * 60)
    maintenance_task_enabled: bool = Field(
        default=True,
        description=(
            "Run periodic background maintenance. "
            "Disable in tests (env MAINTENANCE_TASK_ENABLED=false)."
        ),
    )
    maintenance_interval_seconds: float = Field(
        default=5.0,
        description="Seconds between maintenance runs when enabled.",
    )


settings = Settings()
