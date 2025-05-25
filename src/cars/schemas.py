from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Column
from datetime import datetime, date
import uuid
from enum import Enum

from typing import TypeVar, Generic
from typing import List, Optional




"""Status choice"""
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



"""Pagination"""
T = TypeVar('T')

class ResponseSchema(BaseModel, Generic[T]):  # <- Добавлен Generic[T]
    detail: str
    result: Optional[T] = None

class PageResponse(BaseModel, Generic[T]):
    page_number: int
    page_size: int
    total_pages: int
    total_records: int
    content: List[T]