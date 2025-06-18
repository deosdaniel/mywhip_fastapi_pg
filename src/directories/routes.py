from fastapi import APIRouter, Depends, Query
from src.directories.dependencies import get_dir_service
from src.directories.models import MakesDirectory, ModelsDirectory

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
    order_by: str = Query(
        default="asc", pattern="^(asc|desc)$", description="Порядок сортировки"
    ),
    directory_service: DirectoryService = Depends(get_dir_service),
):
    result = await directory_service.get_all_records(
        MakesDirectory,
        page=page,
        limit=limit,
        sort_by="make",
        order=order_by,
        allowed_sort_fields=["make"],
    )
    return ResponseSchema(detail="Success", result=result)


@directory_router.get(
    "/models",
    response_model=ResponseSchema[PageResponse[ModelSchema]]
    | ResponseSchema[ModelSchema],
)
async def get_all_models(
    page: int = 1,
    limit: int = 10,
    order_by: str = Query(
        default="asc", pattern="^(asc|desc)$", description="Порядок сортировки"
    ),
    directory_service: DirectoryService = Depends(get_dir_service),
):
    result = await directory_service.get_all_records(
        ModelsDirectory,
        page=page,
        limit=limit,
        sort_by="model",
        order=order_by,
        allowed_sort_fields=["model"],
    )
    return ResponseSchema(detail="Success", result=result)


@directory_router.get(
    "/makes/{make_uid}/models",
    response_model=ResponseSchema[PageResponse[ModelSchema]]
    | ResponseSchema[ModelSchema],
)
async def get_models_by_make(
    make_uid: str,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1),
    order_by: str = Query(
        default="asc", pattern="^(asc|desc)$", description="Порядок сортировки"
    ),
    directory_service: DirectoryService = Depends(get_dir_service),
):
    result = await directory_service.get_models_by_make(
        make_uid=make_uid,
        page=page,
        limit=limit,
        sort_by="model",
        order=order_by,
        allowed_sort_fields="model",
    )
    return ResponseSchema(detail="Success", result=result)
