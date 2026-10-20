"""Settings must load valid config and refuse to build without required values."""

import pytest
from pydantic import ValidationError

from app.config import Settings


def test_reads_values_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://u:p@localhost:5432/db")
    monkeypatch.setenv("LLM_MODEL", "some-model:1b")

    # _env_file=None: ignore the developer's real .env so the test is deterministic.
    settings = Settings(_env_file=None)

    assert settings.database_url == "postgresql+psycopg://u:p@localhost:5432/db"
    assert settings.llm_model == "some-model:1b"
    assert settings.ollama_base_url == "http://localhost:11434"  # default kept


def test_missing_database_url_fails_fast(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(ValidationError, match="database_url"):
        Settings(_env_file=None)
