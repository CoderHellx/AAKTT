"""GET /health reports database reachability through the full app.

These tests need no real Postgres:
- "DB up" uses an in-memory SQLite database. `SELECT 1` works on any SQL database, and the
  health check only cares that *a* database answers.
- "DB down" points at a port where nothing listens, so the connection is refused.
"""

from fastapi.testclient import TestClient

from app import __version__
from app.config import Settings
from app.main import create_app

UNREACHABLE_POSTGRES = "postgresql+psycopg://user:pass@127.0.0.1:1/nothing_here"


def make_client(database_url: str) -> TestClient:
    settings = Settings(_env_file=None, database_url=database_url)
    return TestClient(create_app(settings))


def test_health_ok_when_database_answers() -> None:
    response = make_client("sqlite://").get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": __version__, "database": "ok"}


def test_health_503_when_database_unreachable() -> None:
    response = make_client(UNREACHABLE_POSTGRES).get("/health")

    assert response.status_code == 503
    assert response.json() == {
        "status": "unavailable",
        "version": __version__,
        "database": "unreachable",
    }
