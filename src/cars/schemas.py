from pydantic import BaseModel, Field
from datetime import datetime, date
import uuid
from enum import Enum

from typing import List

"""Status choice"""


class CarStatusChoices(Enum):
    FRESH = "FRESH"
    REPAIRING = "REPAIRING"
    DETAILING = "DETAILING"
    LISTED = "LISTED"
    SOLD = "SOLD"


"""Cars"""


class CarCreateSchema(BaseModel):
    make: str = Field(min_length=1)
    model: str = Field(min_length=1)
    year: int = Field(ge=1970, le=int(datetime.now().year))
    vin: str = Field(pattern=r"^[A-HJ-NPR-Z0-9]{10,17}$", default="JTDKB204093488265")
    pts_num: str = Field(
        pattern=r"^[0-9]{2}[А-Яа-яЁё]{2}\s?[0-9]{6}$", default="77ХВ 123456"
    )
    sts_num: str = Field(pattern=r"^[0-9]{4}\s?[0-9]{6}$", default="9955 123456")
    date_purchased: date = Field(default=date.today)
    price_purchased: int = Field(gt=50000)
    status: CarStatusChoices | None = Field(default=CarStatusChoices.FRESH)


class CarCreateResponse(BaseModel):
    uid: uuid.UUID
    owner_uid: uuid.UUID
    make: str
    model: str
    year: int
    vin: str
    pts_num: str
    sts_num: str
    date_purchased: date | None = None
    price_purchased: int = None
    status: CarStatusChoices | None = None


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
    owner_uid: uuid.UUID | None = None
    make: str
    model: str
    year: int
    vin: str
    pts_num: str
    sts_num: str
    date_purchased: date | None = None
    price_purchased: int = None
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
    status: CarStatusChoices | None = Field(default=CarStatusChoices.FRESH)
    expenses: List["ExpensesDTO"] | None = None


"""Expenses"""


class ExpensesCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    exp_summ: int = Field(gt=0)


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


"""Filter schemas"""


class ProdYear(BaseModel):
    year_from: int | None = Field(ge=1970, le=int(datetime.now().year))
    year_to: int | None = Field(ge=1970, le=int(datetime.now().year))


class GetAllFilter(BaseModel):
    page: int = 1
    limit: int = 10
    make: str | None = None
    model: str | None = None
    prod_year: ProdYear | None = None
    status: CarStatusChoices | None = None
    sort_by: str = "created_at"
    order_desc: bool = True
