import logging
from datetime import datetime, timedelta, timezone
from functools import cache
from typing import Annotated
from urllib.parse import urlencode

import httpx
from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config.templates import templates
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


def _create_app_session(
    user: User, expires_in: int, refresh_token: str, id_token: str
) -> tuple[str, datetime]:
    now = datetime.now(timezone.utc)
    expiration = now + timedelta(seconds=expires_in)
    session_id = create_session(user, expiration, refresh_token, id_token)
    return session_id, expiration


class PostLoginRequest(BaseModel):
    access_token: str
    refresh_token: str = ""
    id_token: str = ""
    expires_in: int


@router.post("/auth/login")
async def post_login(
    payload: PostLoginRequest, db: Annotated[Session, Depends(get_db)]
):
    userinfo_url = (
        f"{settings.server_url}/realms/{settings.realm}"
        "/protocol/openid-connect/userinfo"
    )
    userinfo_resp = httpx.get(
        userinfo_url, headers={"Authorization": f"Bearer {payload.access_token}"}
    )

    if userinfo_resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    sub = userinfo_resp.json().get("sub")
    user = _get_user_by_id(db, sub)

    if not user:
        logger.warning(f"Unable to find user: {sub}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    session_id, expiration = _create_app_session(
        user,
        payload.expires_in,
        payload.refresh_token,
        payload.id_token,
    )
    response = JSONResponse({"status": "ok"})
    response.set_cookie(
        "session_id",
        session_id,
        expires=expiration,
        max_age=payload.expires_in,
    )
    return response


@router.get("/auth/callback", name="keycloak_callback")
async def keycloak_callback(request: Request, db: Annotated[Session, Depends(get_db)]):
    token = await oauth_client().keycloak.authorize_access_token(request)

    sub = token.get("userinfo", {}).get("sub")
    user = _get_user_by_id(db, sub)

    if not user:
        request.session["error"] = f"Unable to find user: {sub}"
        return RedirectResponse(request.url_for("error-page"))

    session_id, expiration = _create_app_session(
        user,
        token["expires_in"],
        token.get("refresh_token", ""),
        token.get("id_token", ""),
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
    request: Request,
    session: Annotated[CachedSession | None, Depends(get_optional_session)],
):
    if session is None:
        return templates.TemplateResponse(
            request, "login.html", context={"login": request.url_for("login")}
        )
    else:
        return templates.TemplateResponse(
            request, "home.html", context={"logout": request.url_for("logout")}
        )


@router.get("/error-page", include_in_schema=False, name="error-page")
def error_page(request: Request):
    error = request.session.get("error", "Unexpected error...")
    return templates.TemplateResponse(
        request,
        "error.html",
        context={"logout": request.url_for("logout"), "error": error},
        status_code=500,
    )
