"""GET /health answers through the full app (routing + response model)."""

from fastapi.testclient import TestClient

from app import __version__
from app.config import Settings
from app.main import create_app


def make_client() -> TestClient:
    settings = Settings(_env_file=None, database_url="postgresql+psycopg://test@localhost/test")
    return TestClient(create_app(settings))


def test_health_returns_ok_and_version() -> None:
    response = make_client().get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": __version__}
