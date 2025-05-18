import uuid
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime



class ExpensesSchema(SQLModel):
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now())
    )
    name: str
    exp_summ: int

    car_uid: uuid.UUID = Field(foreign_key="cars.uid")

