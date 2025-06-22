from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime, date
import uuid
from enum import Enum

from typing import List, Literal, Optional

from src.utils.db_types import UUIDString

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
    date_purchased: date = Field(default=date.today, le=date.today())
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
    price_purchased: Optional[int] = Field(default=None, gt=50000)
    date_listed: Optional[date] = Field(default=None, le=date.today())
    price_listed: Optional[int] = Field(default=None, gt=50000)
    date_sold: Optional[date] = Field(default=None, le=date.today())
    price_sold: Optional[int] = Field(default=None, gt=50000)
    autoteka_link: Optional[str] = None
    notes: Optional[str] = Field(default=None, max_length=1000)
    avito_link: Optional[str] = None
    autoru_link: Optional[str] = None
    drom_link: Optional[str] = None
    status: Optional[CarStatusChoices] = None


class CarSchema(BaseModel):
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
    updated_at: datetime | None = created_at
    status: CarStatusChoices | None = Field(default=CarStatusChoices.FRESH)
    expenses: List["ExpensesSchema"] | None = None


"""Expenses"""


class ExpensesCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    exp_summ: int = Field(gt=0)


class UserShortSchema(BaseModel):
    uid: uuid.UUID
    email: str
    username: str


class ExpensesSchema(BaseModel):
    uid: uuid.UUID
    created_at: datetime | None = None
    name: str
    exp_summ: int
    car_uid: uuid.UUID
    user: Optional[UserShortSchema]


"""Filter schemas"""


class ProdYear(BaseModel):
    year_from: int | None = Field(ge=1970, le=int(datetime.now().year))
    year_to: int | None = Field(ge=1970, le=int(datetime.now().year))


class GetAllFilter(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1)
    make: str | None = None
    model: str | None = None
    prod_year: ProdYear | None = None
    status: CarStatusChoices | None = None
    sort_by: Literal[
        "created_at",
        "updated_at",
        "year",
        "make",
        "model",
        "price_purchased",
        "price_listed",
        "price_sold",
        "date_purchased",
        "date_listed",
        "date_sold",
    ] = "created_at"
    order_desc: Literal["desc", "asc"] = "desc"
