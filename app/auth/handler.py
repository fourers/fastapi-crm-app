import logging
from datetime import datetime, timedelta, timezone
from typing import Annotated

from authlib.integrations.base_client.errors import OAuthError
from fastapi import Depends, HTTPException, Request, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.client import get_oauth_client, validate_jwt
from app.auth.session import (
    SSO_IDLE_TIMEOUT_SECONDS,
    SessionType,
    UserSession,
    create_session,
    delete_session,
    log_session_to_state,
)
from app.auth.session import get_session as get_user_session
from app.auth.user import get_user_by_id
from app.utils.hashlib import sha_256
from app.utils.keycloak import get_oauth2_client

BEARER_TOKEN_SESSION_SECONDS = 60
REFRESH_COOKIE_SESSION_THRESHOLD_SECONDS = 60

bearer_token = HTTPBearer(auto_error=False)

logger = logging.getLogger(__name__)


async def _introspect_token(token: str) -> dict:
    metadata = await get_oauth_client().load_server_metadata()
    endpoint = metadata["introspection_endpoint"]
    response = get_oauth2_client().introspect_token(
        endpoint, token=token, token_type_hint="access_token"
    )
    response.raise_for_status()
    return response.json()


def _create_session_from_claims(claims: dict, token: str) -> UserSession | None:
    keycloak_id = claims["sub"]
    user = get_user_by_id(str(keycloak_id))
    if user:
        expiration = min(
            datetime.fromtimestamp(claims["exp"], timezone.utc),
            datetime.now(timezone.utc)
            + timedelta(seconds=BEARER_TOKEN_SESSION_SECONDS),
        )
        session = UserSession(
            session_id=sha_256(token),
            type=SessionType.BEARER,
            id=user.id,
            username=user.username,
            expiration=expiration,
            idle_expiration=expiration,
            refresh_token="xxx",
            id_token="xxx",
        )
        create_session(session)
        return session
    else:
        logger.warning(f"Unable to find user: {keycloak_id}")
        return None


async def _validate_bearer_token(request: Request, token: str) -> UserSession | None:
    try:
        await validate_jwt(token)
    except Exception:
        logger.warning("Failed to validate token", exc_info=True)
        return None

    session = get_user_session(SessionType.BEARER, sha_256(token))
    if session is not None:
        log_session_to_state(request, session)
        return session

    response = await _introspect_token(token)
    active = response["active"]
    if active:
        session = _create_session_from_claims(response, token)
        log_session_to_state(request, session)
        return session
    return None


async def _refresh_token(session: UserSession, idle_timeout: int) -> UserSession:
    metadata = await get_oauth_client().load_server_metadata()
    endpoint = metadata["token_endpoint"]
    response = get_oauth2_client().refresh_token(
        endpoint, refresh_token=session.refresh_token
    )
    session.refresh_token = response["refresh_token"]

    now = datetime.now(timezone.utc)
    session.expiration = now + timedelta(seconds=response["expires_in"])
    session.idle_expiration = now + timedelta(seconds=idle_timeout)

    create_session(session)
    return session


def _end_cookie_session(session: UserSession, response: Response) -> None:
    delete_session(SessionType.COOKIE, session.session_id)
    response.delete_cookie("session_id", httponly=True, secure=True)
    return None


async def _refresh_session(
    session: UserSession, response: Response
) -> UserSession | None:
    try:
        session = await _refresh_token(session, SSO_IDLE_TIMEOUT_SECONDS)
        response.set_cookie(
            "session_id",
            session.session_id,
            expires=session.idle_expiration,
            max_age=SSO_IDLE_TIMEOUT_SECONDS,
            httponly=True,
            secure=True,
        )
        return session
    except OAuthError:
        # End session if cannot be refreshed
        return _end_cookie_session(session, response)


async def _validate_session_id(
    request: Request, session_id: str, response: Response
) -> UserSession | None:
    session = get_user_session(SessionType.COOKIE, session_id)
    if session is None:
        return None
    log_session_to_state(request, session)
    now = datetime.now(timezone.utc)
    if session.idle_expiration < now:
        # End session if SSO session cannot be refreshed
        return _end_cookie_session(session, response)
    elif session.expiration < now:
        return await _refresh_session(session, response)
    else:
        return session


def session_id_cookie(request: Request) -> str | None:
    # Avoid using APIKeyCookie so it doesn't appear in docs
    return request.cookies.get("session_id")


async def get_optional_session(
    request: Request,
    token: Annotated[HTTPAuthorizationCredentials, Depends(bearer_token)],
    session_id: Annotated[str | None, Depends(session_id_cookie)],
    response: Response,
) -> UserSession | None:
    if token is not None:
        return await _validate_bearer_token(request, token.credentials)
    elif session_id is not None:
        return await _validate_session_id(request, session_id, response)
    else:
        return None


def get_session(
    session: Annotated[UserSession | None, Depends(get_optional_session)],
) -> UserSession:
    if session is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return session


async def get_optional_cookie_session(
    request: Request,
    session_id: Annotated[str | None, Depends(session_id_cookie)],
    response: Response,
) -> UserSession | None:
    if session_id is None:
        return None
    return await _validate_session_id(request, session_id, response)


def get_cookie_session(
    session: Annotated[UserSession | None, Depends(get_optional_cookie_session)],
) -> UserSession:
    if session is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return session
