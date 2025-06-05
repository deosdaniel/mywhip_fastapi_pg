from fastapi import APIRouter, Depends, status
from src.db.main import db_session
from src.utils.schemas_common import ResponseSchema, PageResponse
from .schemas import (
    UserCreateSchema,
    UserSchema,
    UserUpdateSchema,
    UserLoginSchema,
)
from .service import UserService
from src.auth.dependencies import get_current_user

user_router = APIRouter()
user_service = UserService()


@user_router.post(
    "/signup",
    response_model=ResponseSchema[UserSchema],
    status_code=status.HTTP_201_CREATED,
)
async def create_user(session: db_session, user_data: UserCreateSchema):
    result = await user_service.create_user(user_data, session)
    return ResponseSchema(detail="Success", result=result)


@user_router.get("/me", response_model=ResponseSchema[UserSchema])
async def get_current_user_info(
    current_user: UserLoginSchema = Depends(get_current_user),
):
    return ResponseSchema(detail="Success", result=current_user)


@user_router.get("/all", response_model=ResponseSchema[PageResponse[UserSchema]])
async def get_all_users(
    session: db_session,
    page: int | None = 1,
    limit: int | None = 10,
):
    result = await user_service.get_all_users(session, page, limit)
    return ResponseSchema(detail="Success", result=result)


@user_router.get("/{user_uid}", response_model=ResponseSchema[UserSchema])
async def get_user_by_uid(session: db_session, user_uid: str) -> dict:
    result = await user_service.get_user_by_uid(user_uid, session)
    return ResponseSchema(detail="Success", result=result)


@user_router.patch("/{user_uid}", response_model=ResponseSchema[UserSchema])
async def update_user(
    session: db_session,
    user_uid: str,
    user_update_data: UserUpdateSchema,
) -> dict:
    result = await user_service.update_user(user_uid, user_update_data, session)
    return ResponseSchema(detail="Success", result=result)


@user_router.delete("/{user_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_uid(user_uid: str, session: db_session):
    await user_service.delete_user(user_uid, session)
    return {}
