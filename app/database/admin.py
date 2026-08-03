from collections.abc import Generator
from contextlib import contextmanager
from functools import cache

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config.database import settings


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


@contextmanager
def _get_admin_db() -> Generator[Session, None, None]:
    db = get_admin_session()()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def provide_db(db: Session | None) -> Generator[Session, None, None]:
    if db is not None:
        yield db
    else:
        with _get_admin_db() as admin_db:
            yield admin_db
