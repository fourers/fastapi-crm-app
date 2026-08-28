from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.handler import get_session
from app.auth.session import UserSession
from app.database.admin import get_db
from app.models.group import Group

router = APIRouter()


class GroupSummary(BaseModel):
    id: int
    name: str


@router.get("/group/{group_id}/subgroup", response_model=list[GroupSummary])
def get_subgroups(
    group_id: int,
    db: Annotated[Session, Depends(get_db)],
    session: Annotated[UserSession, Depends(get_session)],
):
    group = db.get(Group, group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return group.sub_groups
