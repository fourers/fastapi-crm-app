from sqlalchemy import text
from sqlalchemy.orm import Session

from app.auth.session import UserSession

ADMIN_ID = 1


def apply_rls(db: Session, session: UserSession):
    if session.id != ADMIN_ID:
        db.execute(
            text("SELECT set_config('app.current_user_id', :user_id, true)"),
            {"user_id": str(session.id)},
        )
        db.execute(
            text("SELECT set_config('app.enable_rls', :enabled, true)"),
            {"enabled": "true"},
        )
