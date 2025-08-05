from sqlmodel import SQLModel, Field
from uuid import UUID


class CarUserLink(SQLModel, table=True):
    __tablename__ = "car_user_link"
    user_uid: UUID = Field(foreign_key="users.uid", primary_key=True)
    car_uid: UUID = Field(foreign_key="cars.uid", primary_key=True)
