from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.client import Client
from app.session.manager import CachedSession, get_session

router = APIRouter()


@router.get("/client")
def get_clients(
    session: Annotated[CachedSession, Depends(get_session)],
    db: Annotated[Session, Depends(get_db)],
):
    return db.execute(select(Client).order_by(Client.id)).all()


class ClientCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    owner_id: int | None = None


@router.post("/client")
def create_client(
    payload: ClientCreate,
    session: Annotated[CachedSession, Depends(get_session)],
    db: Annotated[Session, Depends(get_db)],
):
    client = Client(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        owner_id=payload.owner_id if payload.owner_id is not None else session.id,
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client
