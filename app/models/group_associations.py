from sqlalchemy import Column, ForeignKey, Integer, Table

from app.models.base import Base

group_users = Table(
    "group_users",
    Base.metadata,
    Column(
        "group_id",
        Integer,
        ForeignKey("groups.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "user_id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
