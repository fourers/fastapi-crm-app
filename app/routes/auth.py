import logging
from datetime import datetime
from typing import Annotated

from authlib.integrations.base_client.errors import OAuthError
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

from app.auth.client import get_oauth_client
from app.auth.handler import (
    get_cookie_session,
    get_optional_cookie_session,
    get_session,
)
from app.auth.session import (
    SSO_IDLE_TIMEOUT_SECONDS,
    SessionType,
    UserSession,
    delete_session,
    log_session_to_state,
)
from app.auth.user import get_user_by_id
from app.auth.verification.cookie import create_cookie_session

logger = logging.getLogger(__name__)

router = APIRouter(tags=["auth"])


@router.get("/login", name="login", include_in_schema=False)
async def keycloak_login(request: Request):
    redirect_uri = request.url_for("login_callback")
    next_param = request.query_params.get("next")
    if next_param:
        redirect_uri = redirect_uri.include_query_params(next=next_param)
    return await get_oauth_client().authorize_redirect(
        request,
        redirect_uri,
    )


def _create_session_from_claims(request: Request, token: dict) -> RedirectResponse:
    sub = token.get("userinfo", {}).get("sub")
    user = get_user_by_id(sub)

    if not user:
        logger.warning(f"Unable to find user: {sub}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    session = create_cookie_session(token, user, SSO_IDLE_TIMEOUT_SECONDS)
    log_session_to_state(request, session)

    redirect_path = request.query_params.get("next", "/")
    request.session.clear()

    response = RedirectResponse(redirect_path)
    response.set_cookie(
        "session_id",
        session.session_id,
        expires=session.idle_expiration,
        max_age=SSO_IDLE_TIMEOUT_SECONDS,
        httponly=True,
        secure=True,
    )
    return response


@router.get("/login/callback", name="login_callback", include_in_schema=False)
async def login_callback(request: Request):
    try:
        token = await get_oauth_client().authorize_access_token(request)
    except OAuthError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return _create_session_from_claims(request, token)


@router.post("/logout", name="logout", include_in_schema=False)
async def logout(
    request: Request,
    session: Annotated[UserSession, Depends(get_optional_cookie_session)],
):
    if session is None:
        return RedirectResponse(request.url_for("home"), 302)
    else:
        return await get_oauth_client().logout_redirect(
            request,
            request.url_for("logout_callback"),
            session.id_token,
        )


@router.get("/logout/callback", name="logout_callback", include_in_schema=False)
async def logout_callback(
    request: Request, session: Annotated[UserSession, Depends(get_cookie_session)]
):
    try:
        await get_oauth_client().validate_logout_response(request)
    except OAuthError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    delete_session(SessionType.COOKIE, session.session_id)
    request.session.clear()

    response = RedirectResponse("/login")
    response.delete_cookie("session_id", httponly=True, secure=True)
    return response


class SessionResponse(BaseModel):
    id: int
    username: str
    created_at: datetime
    refresh_at: Annotated[datetime, Field(alias="expiration")]


@router.get("/me", response_model=SessionResponse)
async def current_session(
    session: Annotated[UserSession, Depends(get_session)],
):
    return session
