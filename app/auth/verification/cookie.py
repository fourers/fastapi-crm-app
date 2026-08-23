from datetime import datetime, timedelta, timezone

from authlib.integrations.base_client.errors import OAuthError
from fastapi import Request, Response

from app.auth.client import get_oauth_client
from app.auth.session import (
    SSO_IDLE_TIMEOUT_SECONDS,
    SessionType,
    UserSession,
    create_session,
    delete_session,
    log_session_to_state,
)
from app.auth.session import get_cached_session as get_user_session
from app.utils.keycloak import get_oauth2_client


async def _refresh_token(session: UserSession, response: Response) -> UserSession:
    metadata = await get_oauth_client().load_server_metadata()
    endpoint = metadata["token_endpoint"]
    refresh_response = get_oauth2_client().refresh_token(
        endpoint, refresh_token=session.refresh_token
    )
    session.refresh_token = refresh_response["refresh_token"]

    now = datetime.now(timezone.utc)
    session.expiration = now + timedelta(seconds=refresh_response["expires_in"])
    session.idle_expiration = now + timedelta(seconds=SSO_IDLE_TIMEOUT_SECONDS)

    create_session(session)

    response.set_cookie(
        "session_id",
        session.session_id,
        expires=session.idle_expiration,
        max_age=SSO_IDLE_TIMEOUT_SECONDS,
        httponly=True,
        secure=True,
    )
    return session


def _end_cookie_session(session: UserSession, response: Response) -> None:
    delete_session(SessionType.COOKIE, session.session_id)
    response.delete_cookie("session_id", httponly=True, secure=True)
    return None


async def _refresh_session(
    session: UserSession, response: Response
) -> UserSession | None:
    try:
        return await _refresh_token(session, response)
    except OAuthError:
        # End session if cannot be refreshed
        return _end_cookie_session(session, response)


async def validate_session_id(
    request: Request, session_id: str, response: Response
) -> UserSession | None:
    session = get_user_session(SessionType.COOKIE, session_id)
    if session is None:
        return None
    log_session_to_state(request, session)
    now = datetime.now(timezone.utc)
    if session.expiration < now:
        return await _refresh_session(session, response)
    else:
        return session
