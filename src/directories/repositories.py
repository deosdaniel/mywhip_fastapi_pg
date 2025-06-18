from typing import Optional

from src.utils.base_service_repo import BaseRepository
from sqlmodel import select
from sqlalchemy import func
from src.directories.models import MakesDirectory, ModelsDirectory


class DirectoryRepository(BaseRepository):

    async def get_models_by_make(
        self,
        make_uid: str,
        offset_page: int,
        limit: int,
        order: str = "desc",
    ) -> list[ModelsDirectory]:
        statement = (
            select(ModelsDirectory)
            .where(ModelsDirectory.make_uid == make_uid)
            .offset(offset_page)
            .limit(limit)
        )
        models = await self.session.exec(statement)
        return models

    async def count_models_by_make(self, make_uid: str):
        result = await self.session.exec(
            select(func.count(ModelsDirectory.uid)).where(
                ModelsDirectory.make_uid == make_uid
            )
        )
        return result.one()

    async def get_single_make(self, requested_make) -> MakesDirectory:
        statement = select(MakesDirectory).where(
            func.lower(MakesDirectory.make) == func.lower(requested_make)
        )
        make = await self.session.exec(statement)
        return make.one_or_none()

    async def get_single_model_by_make(
        self, requested_model, make_uid: str
    ) -> ModelsDirectory:
        statement = (
            select(ModelsDirectory)
            .where(ModelsDirectory.make_uid == make_uid)
            .where(func.lower(ModelsDirectory.model) == func.lower(requested_model))
        )
        model = await self.session.exec(statement)
        return model.one_or_none()
