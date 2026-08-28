from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.handler import get_session
from app.auth.session import UserSession
from app.database.admin import get_db
from app.database.rls import apply_rls
from app.models.client import Client
from app.models.user import User

router = APIRouter()


class OwnerSummary(BaseModel):
    id: int
    owner_id: int


@router.put("/client/{client_id}/owner/{owner_id}", response_model=OwnerSummary)
def update_owner_of_client(
    client_id: int,
    owner_id: int,
    db: Annotated[Session, Depends(get_db)],
    session: Annotated[UserSession, Depends(get_session)],
):
    apply_rls(db, session)
    client = db.get(Client, client_id)
    if not client:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    if client.owner_id == owner_id:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    owner = db.get(User, owner_id)
    if not owner:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Owner id not found")

    client.owner = owner
    db.commit()
    return {
        "id": client_id,
        "owner_id": owner_id,
    }
