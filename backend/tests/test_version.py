from fastapi.testclient import TestClient

from app import __version__
from app.config import Settings
from app.main import create_app


def make_client() -> TestClient:
    settings = Settings(
        app_name="Test-Backend",
        _env_file=None,
        database_url="postgresql+psycopg://test@localhost/test",
    )
    return TestClient(create_app(settings))


def test_get_version_and_print() -> None:
    response = make_client().get("/version")

    assert response.status_code == 200
    assert response.json() == {"app_name": "Test-Backend", "version": __version__}
