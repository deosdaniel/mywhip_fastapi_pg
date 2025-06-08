from src.utils.base_service_repo import BaseRepository
from sqlmodel import select
from sqlalchemy import func
from src.directories.models import MakesDirectory, ModelsDirectory


class DirectoryRepository(BaseRepository):

    async def get_all_makes(self, offset_page: int, limit: int) -> list[MakesDirectory]:
        statement = select(MakesDirectory).offset(offset_page).limit(limit)
        makes = await self.session.exec(statement)
        return makes

    async def get_all_models(
        self, offset_page: int, limit: int
    ) -> list[ModelsDirectory]:
        statement = select(ModelsDirectory).offset(offset_page).limit(limit)
        models = await self.session.exec(statement)
        return models

    async def get_models_by_make(
        self, offset_page: int, limit: int, make_uid: str
    ) -> list[ModelsDirectory]:
        statement = (
            select(ModelsDirectory)
            .where(ModelsDirectory.make_uid == make_uid)
            .offset(offset_page)
            .limit(limit)
        )
        models = await self.session.exec(statement)
        return models

    async def count_all_records_makes(self):
        result = await self.session.exec(select(func.count(MakesDirectory.uid)))
        return result.one()

    async def count_all_records_models(self):
        result = await self.session.exec(select(func.count(ModelsDirectory.uid)))
        return result.one()

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

    async def get_single_model(self, requested_model) -> ModelsDirectory:
        statement = select(ModelsDirectory).where(
            func.lower(ModelsDirectory.model) == func.lower(requested_model)
        )
        model = await self.session.exec(statement)
        return model.one_or_none()

    async def check_model(self, make_uid: str, requested_model: str):
        pass
