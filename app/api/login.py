from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.session.manager import CachedSession, create_session, get_optional_session

sessions = {}  # Replace with Redis or a database

router = APIRouter()


@router.post("/login")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    user = db.query(User).filter_by(username=form_data.username).one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    response = RedirectResponse("/", status_code=303)
    response.set_cookie(
        key="session",
        value=create_session(user),
        httponly=True,
        samesite="lax",
    )
    return response


@router.post("/token")
def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    user = db.query(User).filter_by(username=form_data.username).one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": create_session(user), "token_type": "bearer"}


@router.get("/")
def home(session: Annotated[CachedSession, Depends(get_optional_session)]):
    if session is None:
        return FileResponse("app/static/login.html")
    else:
        return FileResponse("app/static/home.html")
