from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, EmailStr, StringConstraints
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.handler import get_session
from app.auth.session import UserSession
from app.database.admin import get_db
from app.models.user import User
from app.utils.keycloak import create_user as create_keycloak_user

router = APIRouter()


class UserResponse(BaseModel):
    id: int
    email: str | None
    username: str
    first_name: str | None
    last_name: str | None


@router.get("/user", response_model=list[UserResponse])
def get_users(
    db: Annotated[Session, Depends(get_db)],
    session: Annotated[UserSession, Depends(get_session)],
):
    return db.scalars(select(User).order_by(User.id)).all()


class UserUpdate(BaseModel):
    email: Annotated[
        EmailStr | None, StringConstraints(min_length=1, max_length=255)
    ] = None
    first_name: Annotated[
        str | None, StringConstraints(min_length=1, max_length=100)
    ] = None
    last_name: Annotated[
        str | None, StringConstraints(min_length=1, max_length=100)
    ] = None


class UserCreate(UserUpdate):
    username: Annotated[str, StringConstraints(min_length=1, max_length=50)]


@router.post("/user", response_model=UserResponse)
def create_user(
    payload: UserCreate,
    db: Annotated[Session, Depends(get_db)],
    session: Annotated[UserSession, Depends(get_session)],
):
    keycloak_id = create_keycloak_user(
        payload.username, payload.email, payload.first_name, payload.last_name
    )
    user_dict = payload.model_dump(exclude_unset=True)
    user_dict["keycloak_id"] = keycloak_id

    user = User(**user_dict)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.patch("/user/{user_id}", response_model=UserResponse)
def update_user(
    user_id: Annotated[int, Path()],
    payload: UserUpdate,
    db: Annotated[Session, Depends(get_db)],
    session: Annotated[UserSession, Depends(get_session)],
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
