from typing import TYPE_CHECKING

from sqlalchemy import Computed, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.group_associations import group_users

if TYPE_CHECKING:
    from app.models.client import Client
    from app.models.group import Group


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    keycloak_id: Mapped[str] = mapped_column(String(50), unique=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=True)

    clients: Mapped[list["Client"]] = relationship(back_populates="owner")

    groups: Mapped[list["Group"]] = relationship(
        secondary=group_users,
        back_populates="users",
    )

    search_name: Mapped[str] = mapped_column(
        String(255),
        Computed(
            "lower(trim(coalesce(trim(first_name), '') || ' ' || coalesce(trim(last_name), '')))",
            persisted=True,
        ),
        nullable=True,
        index=True,
    )
