import uuid
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime



class ExpensesCreateSchema(SQLModel):
    name: str
    exp_summ: int

class ExpensesSchema(SQLModel):
    uid: uuid.UUID
    created_at: datetime | None = None
    name: str
    exp_summ: int

    car_uid: uuid.UUID

