"""Health check endpoint.

Green means "this instance can actually serve requests", so it checks the database, not just
that the process is up. When the database is unreachable it answers 503 Service Unavailable,
which load balancers and monitors understand as "don't send traffic here".
"""

from typing import Literal

from fastapi import APIRouter, Request, Response, status
from pydantic import BaseModel

from app import __version__
from app.db.engine import database_is_reachable

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    status: Literal["ok", "unavailable"]
    version: str
    database: Literal["ok", "unreachable"]


# A plain `def` (not `async def`): the DB check blocks, so FastAPI runs it in a worker thread
# instead of freezing the event loop that serves every other request.
@router.get("/health", responses={503: {"model": HealthResponse}})
def health(request: Request, response: Response) -> HealthResponse:
    db_ok = database_is_reachable(request.app.state.engine)
    if not db_ok:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return HealthResponse(
        status="ok" if db_ok else "unavailable",
        version=__version__,
        database="ok" if db_ok else "unreachable",
    )
