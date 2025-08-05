from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.sql.functions import now
from datetime import datetime
import uuid

from src.users.schemas import UserRole
from ..shared.car_user_link import CarUserLink

if TYPE_CHECKING:
    from src.cars.models import Cars, Expenses

from ..config import IS_TEST_ENV
from src.utils.db_types import UUIDString

UUIDColumn = UUIDString if IS_TEST_ENV else pg.UUID


class Users(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(
        sa_column=Column(
            UUIDColumn, nullable=False, primary_key=True, default=uuid.uuid4
        )
    )
    role: UserRole = Field(nullable=True, default=UserRole.USER)
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

    cars: list["Cars"] = Relationship(
        back_populates="secondary_owners",
        link_model=CarUserLink,
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    expenses: list["Expenses"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"},
        cascade_delete=True,
    )

    def __repr__(self):
        return f"<Users {self.username})>"
