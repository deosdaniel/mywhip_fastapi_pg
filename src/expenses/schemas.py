import uuid
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime



class ExpensesCreateSchema(SQLModel):
    name: str
    exp_summ: int

class ExpensesSchema(ExpensesCreateSchema):
    uid: uuid.UUID
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))



    car_uid: uuid.UUID = Field(foreign_key="cars.uid")

