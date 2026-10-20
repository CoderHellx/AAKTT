"""Application settings, loaded from environment variables and the repo-root `.env` file.

Every setting is validated once, at startup. A missing or malformed value fails fast with a
clear error instead of surfacing later in the middle of a request.
"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/app/config.py -> parents[2] is the repo root, where .env lives.
REPO_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=REPO_ROOT / ".env",
        env_file_encoding="utf-8",
        # .env also holds POSTGRES_* values meant for Docker, not for us; don't reject them.
        extra="ignore",
    )

    app_name: str = "AAKTT+"

    # Required: no default, so the app refuses to start without it.
    database_url: str = Field(min_length=1)

    ollama_base_url: str = "http://localhost:11434"
    llm_model: str = "qwen3:8b"


@lru_cache
def get_settings() -> Settings:
    """Return the process-wide settings, read from the environment exactly once."""
    return Settings()  # values come from the environment, not arguments
