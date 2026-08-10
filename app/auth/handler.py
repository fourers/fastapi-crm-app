from typing import Annotated

from fastapi import Depends, HTTPException, Request, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.session import (
    UserSession,
)
from app.auth.verification.bearer import validate_bearer_token
from app.auth.verification.cookie import validate_session_id

bearer_token = HTTPBearer(auto_error=False)


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
        return await validate_bearer_token(request, token.credentials)
    elif session_id is not None:
        return await validate_session_id(request, session_id, response)
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
    return await validate_session_id(request, session_id, response)


def get_cookie_session(
    session: Annotated[UserSession | None, Depends(get_optional_cookie_session)],
) -> UserSession:
    if session is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return session
