import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field


class UserCreateSchema(SQLModel):
    username: str = Field(min_length=4, max_length=20)
    email: str = Field(min_length=8, max_length=50)
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=8, max_length=50)


class UserUpdateSchema(SQLModel):
    username: str = Field(min_length=4, max_length=20, default=None)
    first_name: str = Field(min_length=2, max_length=50, default=None)
    last_name: str = Field(min_length=2, max_length=50, default=None)


class UserSchema(SQLModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime | None = None
    updated_at: datetime | None = None
