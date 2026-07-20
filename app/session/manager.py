import secrets
from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyCookie, OAuth2PasswordBearer

from app.models.user import User


@dataclass
class CachedSession:
    id: int
    username: str


sessions: dict[str, CachedSession] = {}


def create_session(user: User) -> str:
    session_id = secrets.token_urlsafe(32)

    sessions[session_id] = CachedSession(
        id=user.id,
        username=user.username,
    )

    return session_id


session_cookie = APIKeyCookie(name="session", auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


def get_optional_session(
    cookie: Annotated[str | None, Security(session_cookie)],
    token: Annotated[str | None, Depends(oauth2_scheme)],
) -> CachedSession | None:
    if token is not None:
        return sessions.get(token)

    if cookie is not None:
        return sessions.get(cookie)

    return None


def get_session(
    cookie: Annotated[str | None, Security(session_cookie)],
    token: Annotated[str | None, Depends(oauth2_scheme)],
) -> CachedSession:
    data = None
    if token is not None:
        data = sessions.get(token)
    elif cookie is not None:
        data = sessions.get(cookie)

    if data is None:
        raise HTTPException(401)

    return data
