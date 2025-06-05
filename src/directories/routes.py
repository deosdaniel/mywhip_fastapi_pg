from fastapi import APIRouter, status, Depends, Path
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session

from src.utils.schemas_common import ResponseSchema, PageResponse
from src.directories.schemas import MakeSchema, ModelSchema
from src.directories.service import DirectoryService

directory_router = APIRouter()
directory_service = DirectoryService()


@directory_router.get(
    "/makes",
    response_model=ResponseSchema[PageResponse[MakeSchema]]
    | ResponseSchema[MakeSchema],
)
async def get_makes(
    session: AsyncSession = Depends(get_session),
    page: int | None = 1,
    limit: int | None = 10,
    requested_make: str | None = None,
):
    result = await directory_service.get_makes(session, page, limit, requested_make)
    return ResponseSchema(detail="Success", result=result)


@directory_router.get(
    "/models",
    response_model=ResponseSchema[PageResponse[ModelSchema]]
    | ResponseSchema[ModelSchema],
)
async def get_models(
    session: AsyncSession = Depends(get_session),
    page: int = 1,
    limit: int = 10,
    requested_model: str | None = None,
):
    result = await directory_service.get_models(session, page, limit, requested_model)
    return ResponseSchema(detail="Success", result=result)
