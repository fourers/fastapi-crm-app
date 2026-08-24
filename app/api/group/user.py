from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.handler import get_session
from app.auth.session import UserSession
from app.database.admin import get_db
from app.models.group import Group
from app.models.user import User

router = APIRouter()


class UserSummary(BaseModel):
    id: int
    username: str


@router.get(
    "/group/{group_id}/user",
    response_model=list[UserSummary],
)
def get_group_users(
    group_id: int,
    db: Annotated[Session, Depends(get_db)],
    session: Annotated[UserSession, Depends(get_session)],
):
    group = db.get(Group, group_id)
    if not group:
        raise HTTPException(status_code=404)

    return group.users


class AssociationSummary(BaseModel):
    group_id: int
    user_id: int


@router.put(
    "/group/{group_id}/user/{user_id}",
    response_model=AssociationSummary,
)
def add_user_to_group(
    group_id: int,
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
    session: Annotated[UserSession, Depends(get_session)],
):
    group = db.get(Group, group_id)
    if not group:
        raise HTTPException(status_code=404)

    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user not in group.users:
        group.users.append(user)
        db.commit()
        return {
            "group_id": group_id,
            "user_id": user_id,
        }

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/group/{group_id}/user/{user_id}",
)
def remove_user_from_group(
    group_id: int,
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
    session: Annotated[UserSession, Depends(get_session)],
):
    group = db.get(Group, group_id)
    if not group:
        raise HTTPException(status_code=404)

    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user in group.users:
        group.users.remove(user)
        db.commit()
        return {
            "group_id": group_id,
            "user_id": user_id,
        }

    return Response(status_code=status.HTTP_204_NO_CONTENT)
