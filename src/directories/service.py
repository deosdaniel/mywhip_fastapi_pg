import math
from sqlalchemy import func
from sqlmodel import select
from src.directories.models import MakesDirectory, ModelsDirectory
from src.utils.exceptions import EntityNotFoundException
from src.utils.schemas_common import PageResponse

from src.utils.base_service import BaseService


class DirectoryService(BaseService):
    async def get_makes(
        self,
        page: int = None,
        limit: int = None,
        requested_make: str = None,
    ):
        if requested_make:
            statement = select(MakesDirectory).where(
                func.lower(MakesDirectory.make) == func.lower(requested_make)
            )
            result = await self.session.exec(statement)
            result = result.first()
            if not result or result == "null":
                raise EntityNotFoundException("Make")
            return result
        else:
            statement = select(MakesDirectory)
            # Pagination
            offset_page = page - 1
            statement = statement.offset(offset_page * limit).limit(limit)
            # Counting records, pages
            count_statement = select(func.count(1)).select_from(MakesDirectory)
            total_records = (await self.session.exec(count_statement)).one() or 0
            total_pages = math.ceil(total_records / limit)
            # Executing query
            result = await self.session.exec(statement)
            result = result.all()
            return PageResponse(
                page_number=page,
                page_size=limit,
                total_pages=total_pages,
                total_records=total_records,
                content=result,
            )

    async def get_models(
        self,
        page: int | None,
        limit: int | None,
        requested_model: str = None,
    ):
        if requested_model:
            statement = select(ModelsDirectory).where(
                func.lower(ModelsDirectory.model) == func.lower(requested_model)
            )
            result = await self.session.exec(statement)
            result = result.first()
            if not result or result == "null":
                raise EntityNotFoundException("Model")
            return result
        else:
            statement = select(ModelsDirectory)
            # Pagination
            offset_page = page - 1
            statement = statement.offset(offset_page * limit).limit(limit)
            # Counting records, pages
            count_statement = select(func.count(1)).select_from(ModelsDirectory)
            total_records = (await self.session.exec(count_statement)).one() or 0
            total_pages = math.ceil(total_records / limit)
            # Executing query
            result = await self.session.exec(statement)
            result = result.all()
            return PageResponse(
                page_number=page,
                page_size=limit,
                total_pages=total_pages,
                total_records=total_records,
                content=result,
            )
