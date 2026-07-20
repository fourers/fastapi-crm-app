from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.client import Client
from app.session.manager import CachedSession, get_session

router = APIRouter()


@router.get("/client")
def get_clients(session: Annotated[CachedSession, Depends(get_session)], db: Annotated[Session, Depends(get_db)]):
    return db.query(Client).all()
