from typing import List

from sqlmodel import SQLModel, Field, Column
from datetime import datetime, date
import uuid
from enum import Enum


class CarStatusChoices(Enum):
    FRESH = 'fresh'
    REPAIRING = 'repairing'
    DETAILING = 'detailing'
    LISTED = 'listed'
    SOLD = 'sold'


"""Cars"""
class CarCreateSchema(SQLModel):
    make: str
    model: str
    year: str
    vin: str
    pts_num: str
    sts_num: str
    date_purchased: date
    price_purchased: int
    expenses: List["ExpensesCreateSchema"] | None = None
    status: CarStatusChoices | None = None
class CarUpdateSchema(SQLModel):
    date_listed: date | None = None
    price_listed: int | None = None
    date_sold: date | None  = None
    price_sold: int | None = None
    autoteka_link: str | None = None
    notes: str | None = None
    avito_link: str | None = None
    autoru_link: str | None = None
    drom_link: str | None = None
    status: CarStatusChoices | None = None

class CarSchema(SQLModel):
    uid: uuid.UUID
    make: str
    model: str
    year: str
    vin: str
    pts_num: str
    sts_num: str
    date_purchased: date
    price_purchased: int
    date_listed: date | None = None
    price_listed: int | None = None
    date_sold: date | None = None
    price_sold: int | None = None
    autoteka_link: str | None = None
    notes: str | None = None
    avito_link: str | None = None
    autoru_link: str | None = None
    drom_link: str | None = None
    created_at: datetime  | None = None
    updated_at: datetime | None = None
    status: CarStatusChoices | None = None


class CarDTO(SQLModel):
    uid: uuid.UUID
    make: str
    model: str
    year: str
    vin: str
    pts_num: str
    sts_num: str
    date_purchased: date
    price_purchased: int
    date_listed: date | None = None
    price_listed: int | None = None
    date_sold: date | None = None
    price_sold: int | None = None
    autoteka_link: str | None = None
    notes: str | None = None
    avito_link: str | None = None
    autoru_link: str | None = None
    drom_link: str | None = None
    created_at: datetime  | None = None
    updated_at: datetime | None = None
    status: CarStatusChoices | None = None
    expenses: List["ExpensesDTO"] | None = None




"""Expenses"""
class ExpensesCreateSchema(SQLModel):
    name: str
    exp_summ: int

class ExpensesSchema(SQLModel):
    uid: uuid.UUID
    created_at: datetime | None = None
    name: str
    exp_summ: int

    car_uid: uuid.UUID


class ExpensesDTO(SQLModel):
    name: str
    exp_summ: int
    created_at: datetime