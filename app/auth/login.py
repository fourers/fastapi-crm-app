import logging
from dataclasses import asdict
from datetime import datetime, timedelta, timezone
from functools import cache
from typing import Annotated
from urllib.parse import urlencode

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from app.auth.handler import get_session
from app.models.user import User
from app.session.manager import (
    UserSession,
    create_session,
    delete_session,
)
from app.session.user import get_user_by_id
from app.utils.keycloak import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", include_in_schema=False)


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


@router.get("/login", name="login")
async def keycloak_login(request: Request):
    return await oauth_client().keycloak.authorize_redirect(
        request,
        request.url_for("keycloak_callback"),
    )


def _create_session_from_claims(user: User, claims: dict) -> tuple[str, datetime]:
    expires_in = claims["expires_in"]
    expiration = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
    session_id = create_session(
        user, expiration, claims["refresh_token"], claims["id_token"]
    )
    return session_id, expiration


@router.get("/callback", name="keycloak_callback")
async def keycloak_callback(request: Request):
    token = await oauth_client().keycloak.authorize_access_token(request)

    sub = token.get("userinfo", {}).get("sub")
    user = get_user_by_id(sub)

    if not user:
        request.session["error"] = f"Unable to find user: {sub}"
        return RedirectResponse(request.url_for("error-page"))

    session_id, expiration = _create_session_from_claims(user, token)
    response = RedirectResponse("/")
    response.set_cookie(
        "session_id",
        session_id,
        expires=expiration,
        max_age=token["expires_in"],
        httponly=True,
        secure=True,
    )
    request.session.clear()
    return response


@router.post("/logout", name="logout")
async def logout(request: Request):
    session_id = request.cookies.get("session_id")
    session = delete_session(session_id)

    metadata = await oauth_client().keycloak.load_server_metadata()
    params = {
        "post_logout_redirect_uri": str(request.url_for("home")),
        "client_id": settings.client_id,
    }
    if session is not None:
        params["id_token_hint"] = session.id_token
    response = RedirectResponse(
        f"{metadata['end_session_endpoint']}?{urlencode(params)}",
        status_code=303,
    )
    response.delete_cookie("session_id", httponly=True, secure=True)
    return response


@router.get("/me")
async def current_session(
    session: Annotated[UserSession, Depends(get_session)],
):
    return asdict(session)
