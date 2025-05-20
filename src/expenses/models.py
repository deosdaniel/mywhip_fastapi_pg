from sqlmodel import Field, Column, SQLModel, Relationship
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.sql.functions import now
import uuid
from datetime import datetime



from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..cars.models import Cars


class Expenses(SQLModel, table=True):
    __tablename__ = "expenses"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    car_uid: uuid.UUID = Field(foreign_key="cars.uid")
    name: str
    exp_summ: int
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=now(), nullable=False))

    car: "Cars" = Relationship(back_populates="expenses")

    def __repr__(self):
        return f'<Expense {self.name}>'