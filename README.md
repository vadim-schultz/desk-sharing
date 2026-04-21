# Desk sharing (MVP)

Monorepo for booking shared office desks by calendar day: **Litestar** + **SQLAlchemy** + **PostgreSQL**, **Vite** + **React** + **Chakra UI**.

## Development

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
export DATABASE_URL=postgresql+psycopg://desk:desk@localhost:5432/desk
export APP_TIMEZONE=Europe/Berlin
alembic upgrade head
python -m scripts.seed
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Set `VITE_API_BASE` to the backend URL (e.g. `http://localhost:8000` for local dev without nginx).

## Production (Docker)

From the repository root:

```bash
docker compose up --build
```

Frontend is on port **80**, API proxied at **`/api`**. Set `APP_TIMEZONE` (default `Europe/Berlin`) and Postgres credentials via environment or `.env`.

## CI

GitHub Actions runs Ruff, Ruff format, Mypy, Pytest (Python 3.11 & 3.12), and frontend `npm run build`.
