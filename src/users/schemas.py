import uuid
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class UserCreateSchema(BaseModel):
    username: str = Field(min_length=4, max_length=20)
    email: EmailStr = Field(min_length=8, max_length=100)
    first_name: str = Field(min_length=2, max_length=50, default=None)
    last_name: str = Field(min_length=2, max_length=50, default=None)
    password: str = Field(min_length=8, max_length=50)


class UserUpdateSchema(BaseModel):
    username: str = Field(min_length=4, max_length=20, default=None)
    first_name: str = Field(min_length=2, max_length=50, default=None)
    last_name: str = Field(min_length=2, max_length=50, default=None)


class UserSchema(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str | None = None
    last_name: str | None = None
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
