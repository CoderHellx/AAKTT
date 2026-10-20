from fastapi import APIRouter, Request
from pydantic import BaseModel

from app import __version__

router = APIRouter(tags=["version"])


class VersionResponse(BaseModel):
    app_name: str
    version: str


@router.get("/version")
def get_version(request: Request) -> VersionResponse:
    settings = request.app.state.settings
    app_name = settings.app_name

    return VersionResponse(app_name=app_name, version=__version__)
