import math


from sqlalchemy import func
from sqlmodel import select
from src.directories.models import MakesDirectory, ModelsDirectory
from src.directories.repositories import DirectoryRepository
from src.utils.exceptions import EntityNotFoundException
from src.utils.schemas_common import PageResponse

from src.utils.base_service_repo import BaseService


class DirectoryService(BaseService[DirectoryRepository]):
    async def get_makes(
        self,
        page: int = None,
        limit: int = None,
    ):

        offset_page = (page - 1) * limit

        makes = await self.repository.get_all_makes(offset_page, limit)
        total_records = await self.repository.count_all_records_makes()
        total_pages = math.ceil(total_records / limit)
        return PageResponse(
            page_number=page,
            page_size=limit,
            total_pages=total_pages,
            total_records=total_records,
            content=makes,
        )

    async def get_single_make(self, requested_make: str):
        make = await self.repository.get_single_make(requested_make)
        if make:
            return make
        else:
            raise EntityNotFoundException("Make")

    async def get_models(
        self,
        page: int | None,
        limit: int | None,
    ):
        offset_page = (page - 1) * limit

        models = await self.repository.get_all_models(offset_page, limit)
        total_records = await self.repository.count_all_records_models()
        total_pages = math.ceil(total_records / limit)
        return PageResponse(
            page_number=page,
            page_size=limit,
            total_pages=total_pages,
            total_records=total_records,
            content=models,
        )

    async def get_single_model(self, requested_model: str):
        model = await self.repository.get_single_model(requested_model)
        if model:
            return model
        else:
            raise EntityNotFoundException("Model")
