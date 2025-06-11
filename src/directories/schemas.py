from pydantic import BaseModel
import uuid


class MakeSchema(BaseModel):
    uid: uuid.UUID
    make: str


class ModelSchema(BaseModel):
    uid: uuid.UUID
    model: str
