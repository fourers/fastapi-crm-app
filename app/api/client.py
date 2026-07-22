from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.rls import apply_rls
from app.models.client import Client
from app.session.manager import CachedSession, get_session

router = APIRouter()


@router.get("/client")
def get_clients(
    db: Annotated[Session, Depends(get_db)],
    session: Annotated[CachedSession, Depends(get_session)],
):
    apply_rls(db, session)
    return db.scalars(select(Client).order_by(Client.id)).all()


class ClientCreate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    owner_id: int | None = None


@router.post("/client")
def create_client(
    payload: ClientCreate,
    db: Annotated[Session, Depends(get_db)],
    session: Annotated[CachedSession, Depends(get_session)],
):
    apply_rls(db, session)
    client_dict = payload.model_dump(exclude_unset=True)
    if client_dict.get("owner_id") is None:
        client_dict["owner_id"] = session.id

    client = Client(**client_dict)
    db.add(client)
    db.commit()
    apply_rls(db, session)
    db.refresh(client)
    return client


@router.patch("/client/{client_id}")
def update_client(
    client_id: Annotated[int, Path()],
    payload: ClientCreate,
    db: Annotated[Session, Depends(get_db)],
    session: Annotated[CachedSession, Depends(get_session)],
):
    apply_rls(db, session)
    client_dict = payload.model_dump(exclude_unset=True)
    client = db.scalars(select(Client).filter_by(id=client_id)).first()
    if not client:
        raise HTTPException(404)

    for key, value in client_dict.items():
        setattr(client, key, value)

    db.commit()
    apply_rls(db, session)
    db.refresh(client)
    return client
