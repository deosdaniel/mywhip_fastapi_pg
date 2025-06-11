from fastapi import APIRouter, Depends, status, Query, HTTPException
from src.utils.schemas_common import ResponseSchema, PageResponse
from .models import Users
from .schemas import (
    UserCreateSchema,
    UserSchema,
    UserUpdateSchema,
    UserRole,
)
from .service import UserService
from .dependencies import get_user_service
from ..auth.dependencies import get_current_user

user_router = APIRouter()


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
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1),
    sort: bool = Query(default=True, case_sensitive=False),
    user_service: UserService = Depends(get_user_service),
):
    result = await user_service.get_all_records(Users, page, limit, sort)
    return ResponseSchema(detail="Success", result=result)


@user_router.get("/{user_uid}", response_model=ResponseSchema[UserSchema])
async def get_user_by_uid(
    user_uid: str,
    user_service: UserService = Depends(get_user_service),
    current_user: UserSchema = Depends(get_current_user),
) -> dict:
    if current_user != UserRole.ADMIN and str(current_user.uid) != user_uid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can not access other user's data",
        )
    result = await user_service.get_by_uid(Users, user_uid)
    return ResponseSchema(detail="Success", result=result)


@user_router.patch("/{user_uid}", response_model=ResponseSchema[UserSchema])
async def update_user(
    user_uid: str,
    user_update_data: UserUpdateSchema,
    user_service: UserService = Depends(get_user_service),
) -> dict:
    result = await user_service.update_by_uid(Users, user_uid, user_update_data)
    return ResponseSchema(detail="Success", result=result)


@user_router.delete("/{user_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_uid(
    user_uid: str, user_service: UserService = Depends(get_user_service)
):
    await user_service.delete_by_uid(Users, user_uid)
    return {}
