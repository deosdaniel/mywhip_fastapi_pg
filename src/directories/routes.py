from fastapi import APIRouter, Depends
from src.directories.dependencies import get_dir_service

from src.utils.schemas_common import ResponseSchema, PageResponse
from src.directories.schemas import MakeSchema, ModelSchema
from src.directories.service import DirectoryService

directory_router = APIRouter()


@directory_router.get(
    "/makes",
    response_model=ResponseSchema[PageResponse[MakeSchema]]
    | ResponseSchema[MakeSchema],
)
async def get_makes(
    page: int | None = 1,
    limit: int | None = 10,
    directory_service: DirectoryService = Depends(get_dir_service),
):
    result = await directory_service.get_makes(page, limit)
    return ResponseSchema(detail="Success", result=result)


@directory_router.get("/makes/{requested_make}")
async def get_single_make(
    requested_make: str | None = None,
    directory_service: DirectoryService = Depends(get_dir_service),
):
    result = await directory_service.get_single_make(requested_make)
    return ResponseSchema(detail="Success", result=result)


@directory_router.get(
    "/models",
    response_model=ResponseSchema[PageResponse[ModelSchema]]
    | ResponseSchema[ModelSchema],
)
async def get_models(
    page: int = 1,
    limit: int = 10,
    directory_service: DirectoryService = Depends(get_dir_service),
):
    result = await directory_service.get_models(page, limit)
    return ResponseSchema(detail="Success", result=result)


@directory_router.get("/makes/{requested_model}")
async def get_single_model(
    requested_model: str | None = None,
    directory_service: DirectoryService = Depends(get_dir_service),
):
    result = await directory_service.get_single_model(requested_model)
    return ResponseSchema(detail="Success", result=result)
