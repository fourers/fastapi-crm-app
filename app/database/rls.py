from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.admin import get_admin_session
from app.session.handler import get_session
from app.session.manager import CachedSession

ADMIN_ID = 1


def get_rls_db(
    session: Annotated[CachedSession, Depends(get_session)],
) -> Generator[Session, None, None]:
    db = get_admin_session()()
    try:
        if session.id != ADMIN_ID:
            db.execute(
                text("SELECT set_config('app.current_user_id', :user_id, false)"),
                {"user_id": str(session.id)},
            )
            db.execute(
                text("SELECT set_config('app.enable_rls', :enabled, false)"),
                {"enabled": "true"},
            )
        yield db
    finally:
        db.close()


def apply_rls(db: Session, session: CachedSession):
    if session.id != ADMIN_ID:
        db.execute(
            text("SELECT set_config('app.current_user_id', :user_id, true)"),
            {"user_id": str(session.id)},
        )
        db.execute(
            text("SELECT set_config('app.enable_rls', :enabled, true)"),
            {"enabled": "true"},
        )
