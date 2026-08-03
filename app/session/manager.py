import logging
import secrets
from datetime import datetime

from pydantic import BaseModel

from app.models.user import User

logger = logging.getLogger(__name__)


class UserSession(BaseModel):
    id: int
    username: str


class CachedSession(UserSession):
    id: int
    username: str
    expiration: datetime
    refresh_token: str
    id_token: str


sessions: dict[str, CachedSession] = {}


def create_session(
    user: User, expiration: datetime, refresh_token: str, id_token: str
) -> str:
    session_id = secrets.token_urlsafe(32)

    sessions[session_id] = CachedSession(
        id=user.id,
        username=user.username,
        expiration=expiration,
        refresh_token=refresh_token,
        id_token=id_token,
    )
    return session_id


def get_session(session_id: str) -> CachedSession | None:
    return sessions.get(session_id)


def delete_session(session_id: str | None) -> CachedSession | None:
    return sessions.pop(session_id, None)


def create_basic_session(user: User) -> UserSession:
    return UserSession(id=user.id, username=user.username)
