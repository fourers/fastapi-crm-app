import secrets
from datetime import datetime, timedelta, timezone
from typing import Annotated

from authlib.integrations.base_client.errors import OAuthError
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

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
    create_session,
    delete_session,
    log_session_to_state,
    refresh_token,
)
from app.auth.user import get_user_by_id
from app.utils.traceback import redirect_error_page

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login", name="login", include_in_schema=False)
async def keycloak_login(request: Request):
    return await get_oauth_client().authorize_redirect(
        request,
        request.url_for("login_callback"),
    )


def _create_session_from_claims(request: Request, token: dict) -> RedirectResponse:
    sub = token.get("userinfo", {}).get("sub")
    user = get_user_by_id(sub)

    if not user:
        return redirect_error_page(request, f"Unable to find user: {sub}")

    now = datetime.now(timezone.utc)
    session_id = secrets.token_urlsafe(32)
    session = UserSession(
        session_id=session_id,
        type=SessionType.COOKIE,
        id=user.id,
        username=user.username,
        expiration=now + timedelta(seconds=token["expires_in"]),
        idle_expiration=now + timedelta(seconds=SSO_IDLE_TIMEOUT_SECONDS),
        refresh_token=token["refresh_token"],
        id_token=token["id_token"],
    )
    create_session(session)
    log_session_to_state(request, session)

    redirect_path = request.session.get("redirect_path", "/")
    request.session.clear()

    response = RedirectResponse(redirect_path)
    response.set_cookie(
        "session_id",
        session_id,
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
    except OAuthError as e:
        return redirect_error_page(request, e.description)

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
    except OAuthError as e:
        return redirect_error_page(request, e.description)

    delete_session(SessionType.COOKIE, session.session_id)
    request.session.clear()

    response = RedirectResponse(request.url_for("home"))
    response.delete_cookie("session_id", httponly=True, secure=True)
    return response


class SessionResponse(BaseModel):
    id: int
    username: str
    expiration: datetime


@router.post(
    "/refresh", response_model=SessionResponse, name="refresh", include_in_schema=False
)
async def refresh(
    session: Annotated[UserSession, Depends(get_cookie_session)],
    response: Response,
):
    try:
        session = await refresh_token(session, SSO_IDLE_TIMEOUT_SECONDS)
    except OAuthError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    response.set_cookie(
        "session_id",
        session.session_id,
        expires=session.idle_expiration,
        max_age=SSO_IDLE_TIMEOUT_SECONDS,
        httponly=True,
        secure=True,
    )
    return session


@router.get("/me", response_model=SessionResponse)
async def current_session(
    session: Annotated[UserSession, Depends(get_session)],
):
    return session
