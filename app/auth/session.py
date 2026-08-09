import logging
from datetime import datetime, timedelta, timezone
from enum import Enum

from fastapi import Request
from pydantic import BaseModel

from app.auth.client import get_oauth_client
from app.utils.keycloak import get_oauth2_client
from app.utils.redis import get_client

logger = logging.getLogger(__name__)

SSO_IDLE_TIMEOUT_SECONDS = 30 * 60


class SessionType(str, Enum):
    BEARER = "bearer"
    COOKIE = "cookie"


class UserSession(BaseModel):
    session_id: str
    type: SessionType
    id: int
    username: str
    expiration: datetime
    idle_expiration: datetime
    refresh_token: str
    id_token: str


def create_session(user_session: UserSession) -> None:
    redis = get_client()
    redis.set(
        name=f"{user_session.type}:{user_session.session_id}",
        value=user_session.model_dump_json(),
        exat=user_session.idle_expiration,
    )


def get_session(session_type: SessionType, session_id: str) -> UserSession | None:
    redis = get_client()
    session = redis.get(f"{session_type}:{session_id}")
    if session is not None:
        try:
            return UserSession.model_validate_json(session)
        except Exception:
            logger.warning("Failed to parse UserSession", exc_info=True)
            redis.delete(f"{session_type}:{session_id}")
    return None


def delete_session(session_type: SessionType, session_id: str) -> None:
    redis = get_client()
    redis.delete(f"{session_type}:{session_id}")


def log_session_to_state(request: Request, session: UserSession | None) -> None:
    if session is not None:
        request.state.user_id = session.id


async def refresh_token(session: UserSession, idle_timeout: int) -> UserSession:
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
