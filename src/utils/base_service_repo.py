import math
from uuid import UUID
from xml.dom.minidom import Entity

from fastapi import HTTPException
from pydantic import BaseModel
from sqlmodel import SQLModel, select, update, desc
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import func

from typing import TypeVar, Generic, Optional, Type

from src.utils.exceptions import EntityNotFoundException
from src.utils.schemas_common import PageResponse


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, table: Type[SQLModel], new_entity_dict: dict) -> SQLModel:
        entity = table(**new_entity_dict)
        self.session.add(entity)
        await self.session.commit()
        return entity

    async def get_by_uid(self, table: SQLModel, uid: str) -> SQLModel:
        fixed_uid = UUID(uid)
        result = await self.session.exec(select(table).where(table.uid == fixed_uid))
        return result.one_or_none()

    async def update_by_uid(
        self, table: SQLModel, uid: str, update_dict: dict
    ) -> Optional[SQLModel]:
        updatable = await self.get_by_uid(table, uid)
        if not updatable:
            return None
        fixed_uid = UUID(uid)
        await self.session.exec(
            update(table).where(table.uid == fixed_uid).values(**update_dict)
        )
        await self.session.commit()
        await self.session.refresh(updatable)
        return updatable

    async def delete_by_uid(self, table: SQLModel, uid: str) -> SQLModel:
        deletable = await self.get_by_uid(table, uid)
        if not deletable:
            return False
        await self.session.delete(deletable)
        await self.session.commit()
        return True

    async def count_all_records(self, table: SQLModel):
        result = await self.session.exec(select(func.count(table.uid)))
        return result.one()

    async def get_all_records(
        self, table: SQLModel, offset_page: int, limit: int, sort: Optional[bool] = None
    ) -> list[SQLModel]:
        statement = select(table).offset(offset_page).limit(limit)
        if sort:
            statement = statement.order_by(desc(table.created_at))
        records = await self.session.exec(statement)
        return records


R = TypeVar("R", bound=BaseRepository)


class BaseService(Generic[R]):
    def __init__(self, repository: R):
        self.repository: R = repository

    async def get_by_uid(self, table: SQLModel, uid: str) -> SQLModel:
        result = await self.repository.get_by_uid(table, uid)
        if result:
            return result
        else:
            raise EntityNotFoundException(f"{table.__name__}-uid")

    async def update_by_uid(
        self, table: SQLModel, uid: str, update_dict: BaseModel
    ) -> SQLModel:
        update_dict = update_dict.model_dump(exclude_unset=True)
        if not update_dict:
            raise HTTPException(status_code=422, detail="Update body cannot be empty")
        updated_entity = await self.repository.update_by_uid(table, uid, update_dict)
        if updated_entity:
            return updated_entity
        else:
            raise EntityNotFoundException(f"{table.__name__}-uid")

    async def delete_by_uid(self, table: SQLModel, uid: str):
        delete_entity = await self.repository.delete_by_uid(table, uid)
        if not delete_entity:
            raise EntityNotFoundException(f"{table.__name__}-uid")
        return True

    async def get_all_records(
        self, table: SQLModel, page: int, limit: int, sort: Optional[bool] = None
    ) -> list[SQLModel]:
        offset_page = (page - 1) * limit

        users = await self.repository.get_all_records(table, offset_page, limit, sort)

        total_records = await self.repository.count_all_records(table)
        total_pages = math.ceil(total_records / limit)

        return PageResponse(
            page_number=page,
            page_size=limit,
            total_pages=total_pages,
            total_records=total_records,
            content=users,
        )
