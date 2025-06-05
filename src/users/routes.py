from fastapi import APIRouter, Depends, status
from src.utils.schemas_common import ResponseSchema, PageResponse
from .schemas import (
    UserCreateSchema,
    UserSchema,
    UserUpdateSchema,
    UserLoginSchema,
)
from .service import UserService
from .dependencies import get_user_service

from src.auth.dependencies import get_current_user


user_router = APIRouter()


# ???????????????
@user_router.get("/me", response_model=ResponseSchema[UserSchema])
async def get_current_user_info(
    current_user: UserLoginSchema = Depends(get_current_user),
):
    return ResponseSchema(detail="Success", result=current_user)


# ???????????????


@user_router.post(
    "/signup",
    response_model=ResponseSchema[UserSchema],
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_data: UserCreateSchema, user_service: UserService = Depends(get_user_service)
):
    result = await user_service.create_user(user_data)
    return ResponseSchema(detail="Success", result=result)


@user_router.get("/all", response_model=ResponseSchema[PageResponse[UserSchema]])
async def get_all_users(
    page: int | None = 1,
    limit: int | None = 10,
    user_service: UserService = Depends(get_user_service),
):
    result = await user_service.get_all_users(page, limit)
    return ResponseSchema(detail="Success", result=result)


@user_router.get("/{user_uid}", response_model=ResponseSchema[UserSchema])
async def get_user_by_uid(
    user_uid: str, user_service: UserService = Depends(get_user_service)
) -> dict:
    result = await user_service.get_user_by_uid(user_uid)
    return ResponseSchema(detail="Success", result=result)


@user_router.patch("/{user_uid}", response_model=ResponseSchema[UserSchema])
async def update_user(
    user_uid: str,
    user_update_data: UserUpdateSchema,
    user_service: UserService = Depends(get_user_service),
) -> dict:
    result = await user_service.update_user(user_uid, user_update_data)
    return ResponseSchema(detail="Success", result=result)


@user_router.delete("/{user_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_uid(
    user_uid: str, user_service: UserService = Depends(get_user_service)
):
    await user_service.delete_user(user_uid)
    return {}
