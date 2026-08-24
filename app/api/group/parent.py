from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.handler import get_session
from app.auth.session import UserSession
from app.database.admin import get_db
from app.models.group import Group

router = APIRouter()


class ParentSummary(BaseModel):
    group_id: int
    parent_id: int


def would_create_parent_cycle(
    group_id: int,
    parent_group: Group,
) -> bool:
    current_group = parent_group
    visited: set[int] = set()

    while current_group is not None:
        current_id = current_group.id
        if current_id == group_id:
            return True

        if current_id in visited:
            # Existing corrupted cycle in the database.
            return True

        visited.add(current_id)

        current_group = parent_group.parent_group

    return False


@router.put("/group/{group_id}/parent/{parent_id}", response_model=ParentSummary)
def update_parent_of_group(
    group_id: int,
    parent_id: int,
    db: Annotated[Session, Depends(get_db)],
    session: Annotated[UserSession, Depends(get_session)],
):
    group = db.get(Group, group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if group_id == parent_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A group cannot be assigned itself as a parent",
        )

    if parent_id == group.parent_id:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    parent_group = db.get(Group, parent_id)
    if not parent_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Parent group not found"
        )

    if would_create_parent_cycle(group_id, parent_group):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A group cannot be assigned beneath one of its descendants",
        )

    group.parent_group = parent_group
    db.commit()
    return {
        "group_id": group_id,
        "parent_id": parent_id,
    }


@router.delete("/group/{group_id}/parent", response_model=ParentSummary)
def remove_parent_from_group(
    group_id: int,
    db: Annotated[Session, Depends(get_db)],
    session: Annotated[UserSession, Depends(get_session)],
):
    group = db.get(Group, group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    old_parent_id = group.parent_id
    if not old_parent_id:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    group.parent_id = None
    db.commit()
    return {
        "group_id": group_id,
        "parent_id": old_parent_id,
    }
