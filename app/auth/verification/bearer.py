import logging
from datetime import datetime, timedelta, timezone

from fastapi import Request

from app.auth.client import get_oauth_client, validate_jwt
from app.auth.session import (
    SessionType,
    UserSession,
    create_session,
    get_session,
    log_session_to_state,
)
from app.auth.user import get_user_by_id
from app.utils.hashlib import sha_256
from app.utils.keycloak import get_oauth2_client

BEARER_TOKEN_SESSION_SECONDS = 60

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


async def validate_bearer_token(request: Request, token: str) -> UserSession | None:
    try:
        await validate_jwt(token)
    except Exception:
        logger.warning("Failed to validate token", exc_info=True)
        return None

    session = get_session(SessionType.BEARER, sha_256(token))
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
