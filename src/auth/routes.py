from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .schemas import UserCreateSchema, UserSchema, UserUpdateSchema
from .service import UserService

auth_router = APIRouter()
user_service = UserService()


@auth_router.post(
    "/signup",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_account(
    user_data: UserCreateSchema, session: AsyncSession = Depends(get_session)
):
    new_user = await user_service.create_user(user_data, session)
    return new_user


@auth_router.get("/all", response_model=List[UserSchema])
async def get_all_users(session: AsyncSession = Depends(get_session)):
    users = await user_service.get_all_users(session)
    return users


@auth_router.get("/{user_uid}", response_model=UserSchema)
async def get_user_by_uid(
    user_uid: str, session: AsyncSession = Depends(get_session)
) -> dict:
    user = await user_service.get_user_by_uid(user_uid, session)
    return user


@auth_router.patch("/{user_uid}", response_model=UserSchema)
async def update_user(
    user_uid: str,
    user_update_data: UserUpdateSchema,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_user = await user_service.update_user(user_uid, user_update_data, session)
    return updated_user


@auth_router.delete("/{user_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_uid(
    user_uid: str, session: AsyncSession = Depends(get_session)
):
    await user_service.delete_user(user_uid, session)
    return {}
