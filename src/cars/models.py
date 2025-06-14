from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlmodel import Field, Column, Relationship, SQLModel
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID, uuid4
from datetime import datetime, date
from sqlalchemy.sql.functions import now
from .schemas import CarStatusChoices

if TYPE_CHECKING:
    from ..users.models import Users


class Cars(SQLModel, table=True):
    __tablename__ = "cars"
    uid: UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid4)
    )
    status: str = Field(
        sa_column=Column(ENUM(CarStatusChoices), default="FRESH", nullable=False)
    )

    make: str
    model: str
    year: int = Field(index=True)
    vin: str
    pts_num: str
    sts_num: str
    date_purchased: date
    price_purchased: int
    date_listed: date = Field(default=None, nullable=True)
    price_listed: int = Field(default=None, nullable=True)
    date_sold: date = Field(default=None, nullable=True)
    price_sold: int = Field(default=None, nullable=True)
    autoteka_link: str = Field(default=None, nullable=True)
    notes: str = Field(default=None, nullable=True)
    avito_link: str = Field(default=None, nullable=True)
    autoru_link: str = Field(default=None, nullable=True)
    drom_link: str = Field(default=None, nullable=True)
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=now(), nullable=False)
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=None, onupdate=now(), nullable=True)
    )
    owner_uid: UUID = Field(
        sa_column=Column(
            pg.UUID,
            ForeignKey("users.uid", ondelete="CASCADE"),
            nullable=True,  # Temporary nullable for tests
            index=True,
        )
    )
    owner: "Users" = Relationship(back_populates="cars")
    expenses: list["Expenses"] = Relationship(
        back_populates="car",
        sa_relationship_kwargs={"lazy": "selectin"},
        cascade_delete=True,
    )

    def __repr__(self):
        return f"<Car {self.vin}>"


class Expenses(SQLModel, table=True):
    __tablename__ = "expenses"
    uid: UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid4)
    )
    name: str
    exp_summ: int
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=now(), nullable=False)
    )
    car_uid: UUID = Field(
        sa_column=Column(
            pg.UUID,
            ForeignKey("cars.uid", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )
    )

    car: "Cars" = Relationship(back_populates="expenses")

    def __repr__(self):
        return f"<Expense {self.name}>"
