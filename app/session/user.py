from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.admin import provide_db
from app.models.user import User


def get_user_by_id(keycloak_id: str, db_session: Session | None = None) -> User | None:
    with provide_db(db_session) as db:
        user = db.scalars(select(User).filter_by(keycloak_id=keycloak_id)).first()
        return user
