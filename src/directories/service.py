import math


from sqlalchemy import func
from sqlmodel import select
from src.directories.models import MakesDirectory, ModelsDirectory
from src.directories.repositories import DirectoryRepository
from src.utils.exceptions import EntityNotFoundException, MakeModelException
from src.utils.schemas_common import PageResponse

from src.utils.base_service_repo import BaseService


class DirectoryService(BaseService[DirectoryRepository]):

    async def get_models_by_make(self, page: int, limit: int, make_uid: str):
        offset_page = (page - 1) * limit

        models = await self.repository.get_models_by_make(offset_page, limit, make_uid)
        total_records = await self.repository.count_models_by_make(make_uid)
        total_pages = math.ceil(total_records / limit)
        return PageResponse(
            page_number=page,
            page_size=limit,
            total_pages=total_pages,
            total_records=total_records,
            content=models,
        )

    async def validate_make_model(self, requested_make: str, requested_model: str):
        make = await self.repository.get_single_make(requested_make)
        if not make:
            raise EntityNotFoundException("Make")
        model = await self.repository.get_single_model_by_make(
            requested_model, make.uid
        )
        if not model:
            raise EntityNotFoundException("Model")
