from fastapi_filter.contrib.sqlalchemy import Filter
from fastapi_filter import FilterDepends, with_prefix
from pydantic import BaseModel
from sqlmodel import SQLModel
from datetime import datetime, date
import uuid
from enum import Enum

from typing import TypeVar, Generic, TYPE_CHECKING
from typing import List, Optional

if TYPE_CHECKING:

    from src.cars.models import Cars

"""Status choice"""


class CarStatusChoices(Enum):
    FRESH = "FRESH"
    REPAIRING = "REPAIRING"
    DETAILING = "DETAILING"
    LISTED = "LISTED"
    SOLD = "SOLD"


"""Filter choice"""


class FilterChoices(Filter):
    make: str | None = None
    model: str | None = None

    class Constants(Filter.Constants):
        model = "Cars"


"""Cars"""


class CarCreateSchema(BaseModel):
    make: str
    model: str
    year: str
    vin: str
    pts_num: str
    sts_num: str
    date_purchased: date
    price_purchased: int
    status: CarStatusChoices | None = None
    expenses: List["ExpensesCreateSchema"] | None = None


class CarUpdateSchema(BaseModel):
    price_purchased: int | None = None
    date_listed: date | None = None
    price_listed: int | None = None
    date_sold: date | None = None
    price_sold: int | None = None
    autoteka_link: str | None = None
    notes: str | None = None
    avito_link: str | None = None
    autoru_link: str | None = None
    drom_link: str | None = None
    status: CarStatusChoices | None = None


class CarSchema(BaseModel):
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
    created_at: datetime | None = None
    updated_at: datetime | None = None
    status: CarStatusChoices | None = None
    expenses: List["ExpensesDTO"] | None = None


"""Expenses"""


class ExpensesCreateSchema(BaseModel):
    name: str
    exp_summ: int


class ExpensesSchema(BaseModel):
    uid: uuid.UUID
    created_at: datetime | None = None
    name: str
    exp_summ: int
    car_uid: uuid.UUID


class ExpensesDTO(BaseModel):
    name: str
    exp_summ: int
    created_at: datetime


"""Pagination"""
T = TypeVar("T")


class ResponseSchema(BaseModel, Generic[T]):
    detail: str
    result: Optional[T] = None


class PageResponse(BaseModel, Generic[T]):
    page_number: int
    page_size: int
    total_pages: int
    total_records: int
    content: List[T]
