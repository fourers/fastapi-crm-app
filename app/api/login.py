from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.session.manager import (
    CachedSession,
    create_session,
    drop_session,
    get_optional_session,
    get_session_id,
)

router = APIRouter(tags=["auth"])


def _get_user_by_username(db: Session, username: str) -> User:
    user = db.scalars(select(User).filter_by(username=username)).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return user


@router.post("/login", include_in_schema=False)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    user = _get_user_by_username(db, form_data.username)

    response = RedirectResponse("/", status_code=303)
    response.set_cookie(
        key="session",
        value=create_session(user),
        httponly=True,
        samesite="lax",
    )
    return response


@router.post("/token")
def post_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    user = _get_user_by_username(db, form_data.username)

    return {"access_token": create_session(user), "token_type": "bearer"}


@router.get("/", include_in_schema=False)
def home(session: Annotated[CachedSession, Depends(get_optional_session)]):
    if session is None:
        return FileResponse("app/static/login.html")
    else:
        return FileResponse("app/static/home.html")


@router.post("/logout")
def logout(session: Annotated[str | None, Depends(get_session_id)]):
    drop_session(session)
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("session")
    return response
