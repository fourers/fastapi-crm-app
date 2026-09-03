from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy import func, select, text
from sqlalchemy.orm import Session

from app.api.types import NullableString, StrictModel
from app.auth.handler import get_session
from app.auth.session import UserSession
from app.database.admin import get_db
from app.models.group import Group

router = APIRouter()


class GroupResponse(BaseModel):
    id: int
    name: str | None
    parent_id: int | None


@router.get("/group", response_model=list[GroupResponse])
def get_groups(
    db: Annotated[Session, Depends(get_db)],
    session: Annotated[UserSession, Depends(get_session)],
):
    return db.scalars(select(Group).order_by(Group.id)).all()


@router.get("/group/search", response_model=list[GroupResponse])
def search_groups(
    q: Annotated[str, Query(min_length=1, max_length=100)],
    db: Annotated[Session, Depends(get_db)],
    session: Annotated[UserSession, Depends(get_session)],
):
    db.execute(text("SET LOCAL pg_trgm.similarity_threshold = 0.1"))
    return db.scalars(
        select(Group)
        .where(Group.name.op("%")(q))
        .order_by(func.similarity(Group.name, q).desc())
    ).all()


@router.get("/group/{group_id}", response_model=GroupResponse)
def get_group(
    group_id: int,
    db: Annotated[Session, Depends(get_db)],
    session: Annotated[UserSession, Depends(get_session)],
):
    group = db.get(Group, group_id)
    if not group:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return group


class GroupCreate(StrictModel):
    name: NullableString = None


@router.post("/group", response_model=GroupResponse)
def create_group(
    payload: GroupCreate,
    db: Annotated[Session, Depends(get_db)],
    session: Annotated[UserSession, Depends(get_session)],
):
    group_dict = payload.model_dump(exclude_unset=True)

    group = Group(**group_dict)
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


@router.patch("/group/{group_id}", response_model=GroupResponse)
def update_group(
    group_id: int,
    payload: GroupCreate,
    db: Annotated[Session, Depends(get_db)],
    session: Annotated[UserSession, Depends(get_session)],
):
    group_dict = payload.model_dump(exclude_unset=True)
    group = db.get(Group, group_id)
    if not group:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    for key, value in group_dict.items():
        setattr(group, key, value)

    db.commit()
    db.refresh(group)
    return group
