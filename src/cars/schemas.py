from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, date
import uuid

class CarCreateSchema(SQLModel):
    status: str = Field(default='fRES', nullable=True)
    make: str
    model: str
    year: str
    vin: str
    pts_num: str
    sts_num: str
    date_purchased: date
    price_purchased: int

class CarUpdateSchema(SQLModel):
    date_listed: date = Field(default=None, nullable=True)
    date_sold: date = Field(default=None, nullable=True)
    price_sold: int = Field(default=None, nullable=True)
    autoteka_link: str = Field(default=None, nullable=True)
    notes: str = Field(default=None, nullable=True)
    avito_link: str = Field(default=None, nullable=True)
    autoru_link: str = Field(default=None, nullable=True)
    drom_link: str = Field(default=None, nullable=True)

class CarSchema(CarCreateSchema, CarUpdateSchema):
    uid: uuid.UUID
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))


