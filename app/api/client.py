from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.types import NullableEmailString, NullableString
from app.auth.handler import get_session
from app.auth.session import UserSession
from app.database.admin import get_db
from app.database.rls import apply_rls
from app.models.client import Client

router = APIRouter()


class ClientResponse(BaseModel):
    id: int
    first_name: str | None
    last_name: str | None
    email: str | None
    owner_id: int | None


@router.get("/client", response_model=list[ClientResponse])
def get_clients(
    db: Annotated[Session, Depends(get_db)],
    session: Annotated[UserSession, Depends(get_session)],
):
    apply_rls(db, session)
    return db.scalars(select(Client).order_by(Client.id)).all()


@router.get("/client/{client_id}", response_model=ClientResponse)
def get_client(
    client_id: int,
    db: Annotated[Session, Depends(get_db)],
    session: Annotated[UserSession, Depends(get_session)],
):
    apply_rls(db, session)
    return db.scalars(select(Client).where(Client.id == client_id)).first()


class ClientCreate(BaseModel):
    first_name: NullableString = None
    last_name: NullableString = None
    email: NullableEmailString = None


@router.post("/client", response_model=ClientResponse)
def create_client(
    payload: ClientCreate,
    db: Annotated[Session, Depends(get_db)],
    session: Annotated[UserSession, Depends(get_session)],
):
    apply_rls(db, session)
    client_dict = payload.model_dump(exclude_unset=True)
    client_dict["owner_id"] = session.id

    client = Client(**client_dict)
    db.add(client)
    db.commit()
    apply_rls(db, session)
    db.refresh(client)
    return client


@router.patch("/client/{client_id}", response_model=ClientResponse)
def update_client(
    client_id: Annotated[int, Path()],
    payload: ClientCreate,
    db: Annotated[Session, Depends(get_db)],
    session: Annotated[UserSession, Depends(get_session)],
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
