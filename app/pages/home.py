from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.auth.handler import get_optional_cookie_session
from app.auth.session import UserSession
from app.config.templates import templates

router = APIRouter(include_in_schema=False)


@router.get("/", include_in_schema=False, name="home")
def home(
    request: Request,
    session: Annotated[UserSession | None, Depends(get_optional_cookie_session)],
):
    if session is None:
        return templates.TemplateResponse(
            request, "login.html", context={"login": request.url_for("login")}
        )
    else:
        return FileResponse("frontend/dist/index.html")


@router.get("/error", include_in_schema=False, name="error-page")
def error_page(request: Request):
    error = request.session.get("error", "Unexpected error...")
    return templates.TemplateResponse(
        request,
        "error.html",
        context={"logout": request.url_for("logout"), "error": error},
        status_code=500,
    )


router.mount("/assets", StaticFiles(directory="frontend/dist/assets"))
