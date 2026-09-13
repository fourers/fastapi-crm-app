from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.event import listens_for
from sqlalchemy.orm import Session

from app.auth.handler import get_session
from app.auth.session import UserSession
from app.database.admin import SessionLocal, _get_engine

ADMIN_ID = 1


def get_rls_db(
    session: Annotated[UserSession, Depends(get_session)],
) -> Generator[Session, None, None]:
    with SessionLocal(bind=_get_engine(), info={"rls_user_id": session.id}) as db:
        yield db


@listens_for(Session, "after_begin")
def set_rls_context(session, transaction, connection):
    user_id = session.info.get("rls_user_id")
    if user_id is None:
        return

    connection.execute(
        text("SELECT set_config('app.current_user_id', :user_id, true)"),
        {"user_id": str(user_id)},
    )
    connection.execute(
        text("SELECT set_config('app.enable_rls', :enabled, true)"),
        {"enabled": "true"},
    )
