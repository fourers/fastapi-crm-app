import logging
from datetime import datetime, timedelta, timezone
from functools import cache
from typing import Annotated
from urllib.parse import urlencode

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.admin import get_db
from app.models.user import User
from app.session.handler import get_optional_session
from app.session.manager import (
    CachedSession,
    create_session,
    delete_session,
)
from app.utils.keycloak import settings

logger = logging.getLogger(__name__)

router = APIRouter(tags=["auth"])
templates = Jinja2Templates(directory="app/static")


@cache
def oauth_client():
    oauth = OAuth()

    oauth.register(
        name="keycloak",
        client_id=settings.client_id,
        server_metadata_url=(
            f"{settings.server_url}/realms/{settings.realm}/.well-known/openid-configuration"
        ),
        client_kwargs={
            "scope": "openid profile email",
            "code_challenge_method": "S256",
        },
    )
    return oauth


@router.get("/auth/login", name="login")
async def keycloak_login(request: Request):
    return await oauth_client().keycloak.authorize_redirect(
        request,
        request.url_for("keycloak_callback"),
    )


def _get_user_by_id(db: Session, keycloak_id: str) -> User | None:
    user = db.scalars(select(User).filter_by(keycloak_id=keycloak_id)).first()
    return user


@router.get("/auth/callback", name="keycloak_callback")
async def keycloak_callback(request: Request, db: Annotated[Session, Depends(get_db)]):
    token = await oauth_client().keycloak.authorize_access_token(request)

    now = datetime.now(timezone.utc)
    sub = token.get("userinfo", {}).get("sub")
    user = _get_user_by_id(db, sub)

    if not user:
        logger.warning(f"Unable to find user: {sub}")
        return RedirectResponse(request.url_for("error-page"))

    expiration = now + timedelta(seconds=token["expires_in"])
    session_id = create_session(
        user, expiration, token.get("refresh_token"), token.get("id_token")
    )

    response = RedirectResponse("/")
    response.set_cookie(
        "session_id",
        session_id,
        expires=expiration,
        max_age=token["expires_in"],
    )
    return response


@router.post("/auth/logout", name="logout")
async def logout(request: Request):
    session_id = request.cookies.get("session_id")
    session = delete_session(session_id)

    if not session:
        response = RedirectResponse("/")
        response.delete_cookie("session_id")
        return response

    metadata = await oauth_client().keycloak.load_server_metadata()
    params = {
        "post_logout_redirect_uri": str(request.url_for("home")),
        "client_id": settings.client_id,
        "id_token_hint": session.id_token,
    }
    response = RedirectResponse(
        f"{metadata['end_session_endpoint']}?{urlencode(params)}",
        status_code=303,
    )
    response.delete_cookie("session_id")
    return response


@router.get("/", include_in_schema=False, name="home")
def home(
    request: Request, session: Annotated[CachedSession, Depends(get_optional_session)]
):
    if session is None:
        return templates.TemplateResponse(request, "login.html", context={
            "login": request.url_for("login")
        })
    else:
        return templates.TemplateResponse(
            request, "home.html", context={"logout": request.url_for("logout")}
        )


@router.get("/error-page", include_in_schema=False, name="error-page")
def error_page(request: Request):
    return templates.TemplateResponse(
        request, "error.html", context={"logout": request.url_for("logout")}
    )
