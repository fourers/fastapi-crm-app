import logging
from datetime import datetime

from pydantic import BaseModel

from app.utils.redis import get_client

logger = logging.getLogger(__name__)


class UserSession(BaseModel):
    session_id: str
    id: int
    username: str
    expiration: datetime
    refresh_token: str
    id_token: str


def create_session(session_type: str, user_session: UserSession) -> None:
    redis = get_client()
    redis.set(
        name=f"{session_type}:{user_session.session_id}",
        value=user_session.model_dump_json(),
        exat=user_session.expiration,
    )


def get_session(session_type: str, session_id: str) -> UserSession | None:
    redis = get_client()
    session = redis.get(f"{session_type}:{session_id}")
    if session is not None:
        try:
            return UserSession.model_validate_json(session)
        except Exception:
            logger.warning("Failed to parse UserSession", exc_info=True)
    return None


def delete_session(session_type: str, session_id: str) -> None:
    redis = get_client()
    redis.delete(f"{session_type}:{session_id}")
