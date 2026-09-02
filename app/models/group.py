from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.group_associations import group_users

if TYPE_CHECKING:
    from app.models.user import User


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True, index=False)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("groups.id"),
        nullable=True,
    )

    parent_group: Mapped["Group | None"] = relationship(
        back_populates="sub_groups",
        remote_side="Group.id",
    )
    sub_groups: Mapped[list["Group"]] = relationship(back_populates="parent_group")

    users: Mapped[list["User"]] = relationship(
        secondary=group_users,
        back_populates="groups",
    )
