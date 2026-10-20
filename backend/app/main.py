"""FastAPI application entry point.

Run locally (from backend/):  uv run uvicorn app.main:create_app --factory --reload

`--factory` tells uvicorn to call create_app() itself. Importing this module therefore has no
side effects (no settings read, no connections opened), which keeps tests and tools safe.
"""

from fastapi import FastAPI

from app import __version__
from app.api import health, version
from app.config import Settings, get_settings


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build a fully configured app.

    A factory (instead of a module-level global built at import time) lets tests construct
    a fresh app with their own settings, with no shared state between tests.
    """
    settings = settings or get_settings()

    application = FastAPI(title=settings.app_name, version=__version__)
    application.state.settings = settings
    application.include_router(health.router)
    application.include_router(version.router)
    return application
