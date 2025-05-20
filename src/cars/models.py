from sqlmodel import Field, Column, Relationship, SQLModel
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime, date


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..expenses.models import Expenses


class Cars(SQLModel, table=True):
    __tablename__ = "cars"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    status: str = Field(default='Fresh', nullable=False)
    make: str
    model: str
    year: str
    vin: str
    pts_num: str
    sts_num: str
    date_purchased: date
    price_purchased: int

    date_listed: date = Field(default=None, nullable=True)
    date_sold: date = Field(default=None, nullable=True)
    price_sold: int = Field(default=None, nullable=True)
    autoteka_link: str = Field(default=None, nullable=True)
    notes: str = Field(default=None, nullable=True)
    avito_link: str = Field(default=None, nullable=True)
    autoru_link: str = Field(default=None, nullable=True)
    drom_link: str = Field(default=None, nullable=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=None, nullable=True))

    expenses: list["Expenses"] = Relationship(back_populates="car")

    def __repr__(self):
        return f'<Car {self.vin}>'

