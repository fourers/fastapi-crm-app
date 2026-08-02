from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyCookie

from app.session.manager import CachedSession
from app.session.manager import get_session as get_cached_session

session_id_cookie = APIKeyCookie(name="session_id", auto_error=False)


def get_optional_session(
    session_id: Annotated[str, Depends(session_id_cookie)],
) -> CachedSession | None:
    now = datetime.now(timezone.utc)
    session = get_cached_session(session_id)
    if session is not None and session.expiration > now:
        return session
    else:
        return None


def get_session(
    session: Annotated[CachedSession | None, Depends(get_optional_session)],
) -> CachedSession:
    if session is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return session
