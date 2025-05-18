from sqlmodel import Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
import uuid
from .schemas import CarSchema

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..expenses.models import Expenses


class Cars(CarSchema, table=True):
    __tablename__ = "cars"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    expenses: list["Expenses"] = Relationship(back_populates="car")

    def __repr__(self):
        return f'<Car {self.vin}>'

