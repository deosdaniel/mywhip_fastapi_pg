from tkinter.filedialog import FileDialog

from pydantic import BaseModel, Field
from sqlmodel import SQLModel
from datetime import datetime, date
import uuid
from enum import Enum

from typing import TypeVar, Generic, TYPE_CHECKING
from typing import List, Optional


"""Status choice"""


class CarStatusChoices(Enum):
    FRESH = "FRESH"
    REPAIRING = "REPAIRING"
    DETAILING = "DETAILING"
    LISTED = "LISTED"
    SOLD = "SOLD"


"""Cars"""


class CarCreateSchema(BaseModel):
    make: str
    model: str
    year: int = Field(ge=1970, le=int(datetime.now().year))
    vin: str = Field(min_length=10, max_length=17)
    pts_num: str = Field(pattern=r"^[0-9]{2}\s?[А-Яа-яЁё]{2}\s?[0-9]{6}$")
    sts_num: str = Field(pattern=r"^[0-9]{4}\s?[0-9]{6}$")
    date_purchased: date | None = Field(default=date.today)
    price_purchased: int = Field(gt=50000)
    status: CarStatusChoices | None = Field(default=CarStatusChoices.FRESH)
    expenses: List["ExpensesCreateSchema"] | None = None


class CarUpdateSchema(BaseModel):
    price_purchased: int | None = Field(gt=50000)
    date_listed: date | None = None
    price_listed: int | None = Field(gt=50000)
    date_sold: date | None = None
    price_sold: int | None = Field(gt=50000)
    autoteka_link: str | None = None
    notes: str | None = Field(max_length=1000)
    avito_link: str | None
    autoru_link: str | None = None
    drom_link: str | None = None
    status: CarStatusChoices | None = None


class CarSchema(BaseModel):
    uid: uuid.UUID
    make: str
    model: str
    year: int = Field(ge=1970, le=int(datetime.now().year))
    vin: str = Field(min_length=10, max_length=17)
    pts_num: str = Field(pattern=r"^[0-9]{2}\s?[А-Яа-яЁё]{2}\s?[0-9]{6}$")
    sts_num: str = Field(pattern=r"^[0-9]{4}\s?[0-9]{6}$")
    date_purchased: date | None = Field(default=date.today)
    price_purchased: int = Field(gt=50000)
    date_listed: date | None = None
    price_listed: int | None = Field(gt=50000)
    date_sold: date | None = None
    price_sold: int | None = Field(gt=50000)
    autoteka_link: str | None = None
    notes: str | None = None
    avito_link: str | None = None
    autoru_link: str | None = None
    drom_link: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    status: CarStatusChoices | None = Field(default=CarStatusChoices.FRESH)
    expenses: List["ExpensesDTO"] | None = None


"""Expenses"""


class ExpensesCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    exp_summ: int = Field(gt=0)


class ExpensesSchema(BaseModel):
    uid: uuid.UUID
    created_at: datetime | None = None
    name: str = Field(min_length=1, max_length=50)
    exp_summ: int = Field(gt=0)
    car_uid: uuid.UUID


class ExpensesDTO(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    exp_summ: int = Field(gt=0)
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


"""Filter schemas"""


class ProdYear(BaseModel):
    year_from: int | None = None
    year_to: int | None = None


class GetAllSchema(BaseModel):
    page: int = 1
    limit: int = 10
    make: str | None = None
    model: str | None = None
    prod_year: ProdYear | None = None
    status: CarStatusChoices | None = None
    sort_by: str = "created_at"
    order_desc: bool = True
