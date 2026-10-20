# AAKTT+ — Adaptive Agentic Knowledge-Tracing Tutor

A tutor that turns a document or topic into a graph of concepts, works out what you already know, and teaches exactly the gaps.

- **Design and roadmap:** [ARCHITECTURE.md](ARCHITECTURE.md)
- **Status:** Phase 1, milestone 1 (project skeleton)

## Run locally

Prerequisites: Python 3.13, [uv](https://docs.astral.sh/uv/) on your PATH, Docker Desktop running.

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
