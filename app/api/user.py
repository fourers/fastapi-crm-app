from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.admin import get_db
from app.models.user import User
from app.session.handler import get_session
from app.session.manager import CachedSession
from app.utils.keycloak import create_user as create_keycloak_user

router = APIRouter()


@router.get("/user/me")
def current_session(
    session: Annotated[CachedSession, Depends(get_session)],
):
    return asdict(session)


@router.get("/user")
def get_users(
    session: Annotated[CachedSession, Depends(get_session)],
    db: Annotated[Session, Depends(get_db)],
):
    return db.scalars(select(User).order_by(User.id)).all()


class UserUpdate(BaseModel):
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None


class UserCreate(UserUpdate):
    username: str


@router.post("/user")
def create_user(
    payload: UserCreate,
    db: Annotated[Session, Depends(get_db)],
):
    create_keycloak_user(
        payload.username, payload.email, payload.first_name, payload.last_name
    )
    user_dict = payload.model_dump(exclude_unset=True)

    user = User(**user_dict)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.patch("/user/{user_id}")
def update_user(
    user_id: Annotated[int, Path()],
    payload: UserUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    user_dict = payload.model_dump(exclude_unset=True)
    user = db.scalars(select(User).filter_by(id=user_id)).first()
    if not user:
        raise HTTPException(404)

    for key, value in user_dict.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user
