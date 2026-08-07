from collections.abc import Generator
from contextlib import contextmanager
from functools import cache

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config.database import settings

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


@cache
def _get_engine() -> Engine:
    return create_engine(settings.database_url)


def get_db() -> Generator[Session, None, None]:
    with SessionLocal(bind=_get_engine()) as db:
        yield db


@contextmanager
def provide_db(db: Session | None) -> Generator[Session, None, None]:
    if db is not None:
        yield db
    else:
        with SessionLocal(bind=_get_engine()) as session:
            yield session
