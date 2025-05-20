import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field



class UserCreateSchema(SQLModel):
    username: str = Field(min_length=4, max_length=20, unique=True)
    email: str = Field(min_length=8, max_length=50, unique=True)
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    password: str

class UserUpdateSchema(SQLModel):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None

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
