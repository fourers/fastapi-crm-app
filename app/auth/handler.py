import logging
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from async_lru import alru_cache
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient

from app.auth.client import get_oauth_client
from app.auth.session import (
    SessionType,
    UserSession,
    create_session,
)
from app.auth.session import (
    get_session as get_user_session,
)
from app.config.keycloak import settings
from app.session.user import get_user_by_id
from app.utils.hashlib import sha_256
from app.utils.keycloak import get_oauth2_client

bearer_token = HTTPBearer(auto_error=False)

logger = logging.getLogger(__name__)


@alru_cache
async def _get_jwk_keys() -> PyJWKClient:
    metadata = await get_oauth_client().load_server_metadata()
    endpoint = metadata["jwks_uri"]
    return PyJWKClient(endpoint)


async def _validate_jwt(token: str) -> None:
    jwk_keys = await _get_jwk_keys()
    jwt.decode(
        token,
        key=jwk_keys.get_signing_key_from_jwt(token),
        algorithms=["RS256"],
        options={
            "require": ["iss", "aud", "exp"],
            "verify_iss": True,
            "verify_aud": True,
            "verify_exp": True,
        },
        issuer=f"{settings.server_url}/realms/{settings.realm}",
        audience=settings.client_id,
    )


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
            datetime.now(timezone.utc) + timedelta(seconds=60),
        )
        session = UserSession(
            session_id=sha_256(token),
            type=SessionType.BEARER,
            id=user.id,
            username=user.username,
            expiration=expiration,
            refresh_token="xxx",
            id_token="xxx",
        )
        create_session(session)
        return session
    else:
        logger.warning(f"Unable to find user: {keycloak_id}")
        return None


async def _validate_bearer_token(token: str) -> UserSession | None:
    try:
        await _validate_jwt(token)
    except Exception:
        logger.warning("Failed to validate token", exc_info=True)
        return None

    session = get_user_session(SessionType.BEARER, sha_256(token))
    if session is not None:
        return session

    response = await _introspect_token(token)
    active = response["active"]
    if active:
        return _create_session_from_claims(response, token)
    return None


def _validate_session_id(session_id: str) -> UserSession | None:
    return get_user_session(SessionType.COOKIE, session_id)


def session_id_cookie(request: Request) -> str | None:
    # Avoid using APIKeyCookie so it doesn't appear in docs
    return request.cookies.get("session_id")


async def get_optional_session(
    token: Annotated[HTTPAuthorizationCredentials, Depends(bearer_token)],
    session_id: Annotated[str | None, Depends(session_id_cookie)],
) -> UserSession | None:
    if token is not None:
        return await _validate_bearer_token(token.credentials)
    elif session_id is not None:
        return _validate_session_id(session_id)
    else:
        return None


def get_session(
    session: Annotated[UserSession | None, Depends(get_optional_session)],
) -> UserSession:
    if session is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return session


def get_optional_cookie_session(
    session_id: Annotated[str | None, Depends(session_id_cookie)],
) -> UserSession | None:
    if session_id is None:
        return None
    return _validate_session_id(session_id)


def get_cookie_session(
    session: Annotated[UserSession | None, Depends(get_optional_cookie_session)],
) -> UserSession:
    if session is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return session
