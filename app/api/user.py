from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Depends

from app.session.manager import CachedSession, get_session

router = APIRouter()


@router.get("/user/me")
def get_clients(
    session: Annotated[CachedSession, Depends(get_session)],
):
    return asdict(session)
