from fastapi import APIRouter, Depends, Query
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
async def get_all_makes(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1),
    directory_service: DirectoryService = Depends(get_dir_service),
):
    result = await directory_service.get_all_makes(page, limit)
    return ResponseSchema(detail="Success", result=result)


@directory_router.get(
    "/models",
    response_model=ResponseSchema[PageResponse[ModelSchema]]
    | ResponseSchema[ModelSchema],
)
async def get_all_models(
    page: int = 1,
    limit: int = 10,
    directory_service: DirectoryService = Depends(get_dir_service),
):
    result = await directory_service.get_all_models(page, limit)
    return ResponseSchema(detail="Success", result=result)


@directory_router.get(
    "/models/{make_uid}",
    response_model=ResponseSchema[PageResponse[ModelSchema]]
    | ResponseSchema[ModelSchema],
)
async def get_models_by_make(
    page: int = 1,
    limit: int = 10,
    make_uid: str | None = None,
    directory_service: DirectoryService = Depends(get_dir_service),
):
    result = await directory_service.get_models_by_make(page, limit, make_uid)
    return ResponseSchema(detail="Success", result=result)


# @directory_router.get("/models/{requested_model}")
# async def get_single_model(
#    requested_model: str | None = None,
#    directory_service: DirectoryService = Depends(get_dir_service),
# ):
#    result = await directory_service.get_single_model(requested_model)
#    return ResponseSchema(detail="Success", result=result)
#

# @directory_router.get("/makes/{requested_make}")
# async def get_single_make(
#    requested_make: str | None = None,
#    directory_service: DirectoryService = Depends(get_dir_service),
# ):
#    result = await directory_service.get_single_make(requested_make)
#    return ResponseSchema(detail="Success", result=result)
#
