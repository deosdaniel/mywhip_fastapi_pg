from sqlmodel import Field, Column, Relationship, SQLModel
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime, date
from sqlalchemy.sql.functions import now



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
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=now(), nullable=False))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=None, onupdate=now(), nullable=True))

    expenses: list["Expenses"] = Relationship(back_populates="car", sa_relationship_kwargs={'lazy':'selectin'}, cascade_delete=True)

    def __repr__(self):
        return f'<Car {self.vin}>'


class Expenses(SQLModel, table=True):
    __tablename__ = "expenses"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    name: str
    exp_summ: int
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=now(), nullable=False))

    car_uid: uuid.UUID = Field(foreign_key="cars.uid")
    car: "Cars" = Relationship(back_populates="expenses")

    def __repr__(self):
        return f'<Expense {self.name}>'