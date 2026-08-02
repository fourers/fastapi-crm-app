import logging
import secrets
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyCookie

from app.models.user import User

logger = logging.getLogger(__name__)


@dataclass
class CachedSession:
    id: int
    username: str
    expiration: datetime
    refresh_token: str


sessions: dict[str, CachedSession] = {}


def create_session(user: User, expiration: datetime, refresh_token: str) -> str:
    session_id = secrets.token_urlsafe(32)

    sessions[session_id] = CachedSession(
        user.id,
        user.username,
        expiration,
        refresh_token,
    )
    return session_id


def delete_session(session_id: str | None) -> CachedSession | None:
    return sessions.pop(session_id, None)


session_id_cookie = APIKeyCookie(name="session_id", auto_error=False)


def get_optional_session(
    session_id: Annotated[str, Depends(session_id_cookie)],
) -> CachedSession | None:
    logger.info(f"Sessions: {sessions}")
    now = datetime.now(timezone.utc)
    session = sessions.get(session_id)
    if session is not None and session.expiration > now:
        logger.info(f"Session found: {session}")
        return session
    else:
        logger.warning(f"No session found for {session_id}: {session}")
        return None


def get_session(
    session: Annotated[CachedSession | None, Depends(get_optional_session)],
) -> CachedSession:
    if session is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return session
