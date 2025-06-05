from pydantic import BaseModel
from typing import TypeVar, Generic
from typing import List, Optional


"""Pagination"""
T = TypeVar("T")


class ResponseSchema(BaseModel, Generic[T]):
    detail: str
    result: Optional[T] = None


class PageResponse(BaseModel, Generic[T]):
    page_number: int
    page_size: int
    total_pages: int
    total_records: int
    content: List[T]
