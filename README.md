# AAKTT+ — Adaptive Agentic Knowledge-Tracing Tutor

A tutor that turns a document or topic into a graph of concepts, works out what you already know, and teaches exactly the gaps.

- **Design and roadmap:** [ARCHITECTURE.md](ARCHITECTURE.md)
- **Ubuntu setup:** [docs/setup-ubuntu.md](docs/setup-ubuntu.md)

## Current status

**Phase 1, milestone 1: project skeleton.**

| Step | What | State |
|---|---|---|
| 1 | Git, `.gitignore`, `.env.example` | ✅ |
| 2 | uv project, pytest, ruff, mypy (strict) | ✅ |
| 3 | FastAPI app factory, validated settings, `/health`, `/version` | ✅ |
| 4 | Postgres in Docker Compose, `/health` checks the DB (503 when down) | ✅ |
| 5 | GitHub Actions CI: tests, lint and types on every push, with a real Postgres | ⏭️ next |

## Run locally

Prerequisites: Python 3.13, [uv](https://docs.astral.sh/uv/) on your PATH, Docker running.

```bash
cp .env.example .env        # once, then edit values if needed
docker compose up -d --wait # start Postgres (from the repo root) and wait until it's healthy
cd backend                  # uv commands must run here, where pyproject.toml lives
uv run uvicorn app.main:create_app --factory --reload
```

Then open http://localhost:8000/docs (Swagger UI) or http://localhost:8000/health.

## Checks

From `backend/`:

```bash
uv run pytest
uv run ruff check . && uv run ruff format --check .
uv run mypy app tests
```
