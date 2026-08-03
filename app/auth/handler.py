from datetime import datetime, timezone
from typing import Annotated

import httpx
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyCookie, OAuth2PasswordBearer

from app.config.keycloak import settings
from app.session.manager import CachedSession, UserSession, create_basic_session
from app.session.manager import get_session as get_cached_session
from app.session.user import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)
session_id_cookie = APIKeyCookie(name="session_id", auto_error=False)


def _validate_bearer_token(token: str) -> UserSession | None:
    userinfo_endpoint = (
        f"{settings.server_url}/realms/{settings.realm}"
        "/protocol/openid-connect/userinfo"
    )
    response = httpx.get(
        userinfo_endpoint, headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code != httpx.codes.OK:
        return None
    keycloak_id = response.json()["sub"]
    user = get_user_by_id(keycloak_id)
    if not user:
        return None
    return create_basic_session(user)


def _validate_session(session: CachedSession | None) -> bool:
    return session is not None and session.expiration > datetime.now(timezone.utc)


def _validate_session_id(cookie: str):
    session = get_cached_session(cookie)
    return session if _validate_session(session) else None


def get_optional_session(
    token: Annotated[str, Depends(oauth2_scheme)],
    session_id: Annotated[str, Depends(session_id_cookie)],
) -> UserSession | None:
    if token is not None:
        return _validate_bearer_token(token)
    else:
        return _validate_session_id(session_id)


def get_session(
    session: Annotated[UserSession | None, Depends(get_optional_session)],
) -> UserSession:
    if session is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return session


def get_cookie_session(
    session_id: Annotated[str, Depends(session_id_cookie)],
) -> CachedSession | None:
    return _validate_session_id(session_id)
