from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from app.auth.handler import get_optional_cookie_session
from app.auth.session import UserSession

router = APIRouter(include_in_schema=False)


@router.get("/{path:path}", name="catch-all")
def catch_all(
    session: Annotated[UserSession | None, Depends(get_optional_cookie_session)],
):
    return FileResponse("frontend/dist/index.html")
