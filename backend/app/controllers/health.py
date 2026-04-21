from litestar import get


@get("/health", sync_to_thread=False)
def health_check() -> dict[str, str]:
    return {"status": "ok"}
