from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.sql.functions import now
from datetime import datetime
import uuid


class Users(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    username: str = Field(unique=True, nullable=False)
    email: str = Field(unique=True, nullable=False, index=True)
    first_name: str = Field(nullable=True)
    last_name: str = Field(nullable=True)
    is_verified: bool = Field(default=False)
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=now(), nullable=False)
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=None, onupdate=now(), nullable=True)
    )

    def __repr__(self):
        return f"<Users {self.username})>"
