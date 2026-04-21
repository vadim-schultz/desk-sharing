from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://desk:desk@localhost:5432/desk"
    app_timezone: str = "Europe/Berlin"


settings = Settings()
