"""FastAPI application entry point.

Run locally (from backend/):  uv run uvicorn app.main:create_app --factory --reload

`--factory` tells uvicorn to call create_app() itself. Importing this module therefore has no
side effects (no settings read, no connections opened), which keeps tests and tools safe.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import __version__
from app.api import health, version
from app.config import Settings, get_settings
from app.db.engine import build_engine


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build a fully configured app.

    A factory (instead of a module-level global built at import time) lets tests construct
    a fresh app with their own settings, with no shared state between tests.
    """
    settings = settings or get_settings()
    engine = build_engine(settings.database_url)  # lazy: no connection opened yet

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        # Code before `yield` runs at startup, code after it at shutdown.
        yield
        engine.dispose()  # close pooled connections cleanly

    application = FastAPI(title=settings.app_name, version=__version__, lifespan=lifespan)
    application.state.settings = settings
    application.state.engine = engine
    application.include_router(health.router)
    application.include_router(version.router)
    return application
