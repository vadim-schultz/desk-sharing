"""CORS configuration for the Litestar app (wired via `cors_config=...`)."""

from litestar.config.cors import CORSConfig

cors_config = CORSConfig(
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
