from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.auth.handler import get_optional_cookie_session
from app.auth.session import UserSession

FRONTEND_FILE_PATH = "frontend/dist/index.html"

router = APIRouter(include_in_schema=False)
router.mount("/assets", StaticFiles(directory="frontend/dist/assets"))


@router.get("/{path:path}", name="catch-all")
def catch_all(
    session: Annotated[UserSession | None, Depends(get_optional_cookie_session)],
):
    return FileResponse(FRONTEND_FILE_PATH)
