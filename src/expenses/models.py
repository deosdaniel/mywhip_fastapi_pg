from sqlmodel import Field, Column, SQLModel, Relationship
import sqlalchemy.dialects.postgresql as pg
import uuid
from .schemas import ExpensesSchema

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..cars.models import Cars


class Expenses(ExpensesSchema, table=True):
    __tablename__ = "expenses"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    car: "Cars" = Relationship(back_populates="expenses")

    def __repr__(self):
        return f'<Expense {self.name}>'