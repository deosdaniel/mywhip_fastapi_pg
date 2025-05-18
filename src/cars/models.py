from sqlmodel import Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid

from .schemas import CarSchema

class Cars(CarSchema, table=True):
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    def __repr__(self):
        return f'<Car {self.vin}>'

