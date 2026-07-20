from collections.abc import Generator
from functools import cache

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings


@cache
def get_admin_session() -> sessionmaker:
    engine = create_engine(settings.database_url)

    return sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )


def get_db() -> Generator[Session, None, None]:
    db = get_admin_session()()
    try:
        yield db
    finally:
        db.close()
