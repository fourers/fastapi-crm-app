from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.auth.handler import get_optional_cookie_session
from app.auth.session import UserSession
from app.config.templates import templates

FRONTEND_FILE_PATH = "frontend/dist/index.html"

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
        return FileResponse(FRONTEND_FILE_PATH)


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


@router.get("/{path:path}", name="catch-all")
def catch_all(
    request: Request,
    session: Annotated[UserSession | None, Depends(get_optional_cookie_session)],
):
    if session is None:
        url = request.url.path
        if request.url.query:
            url = f"{url}?{request.url.query}"
        request.session["redirect_path"] = url
        return RedirectResponse("/")
    else:
        return FileResponse(FRONTEND_FILE_PATH)
