"""Health check endpoint.

For now this only answers "is the process up?". Milestone 1, step 4 extends it to check the
database, so a green health check means the app can actually serve requests.
"""

from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

from app import __version__

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    status: Literal["ok"]
    version: str


@router.get("/health")
def health() -> HealthResponse:
    return HealthResponse(status="ok", version=__version__)
