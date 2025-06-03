from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .deps import get_current_user
from .models import Users
from .schemas import (
    UserCreateSchema,
    UserSchema,
    UserUpdateSchema,
    UserLoginSchema,
    ResponseSchema,
    PageResponse,
)
from .service import UserService
from .utils import create_access_token
from fastapi.responses import JSONResponse


auth_router = APIRouter()
user_service = UserService()


@auth_router.post(
    "/signup",
    response_model=ResponseSchema[UserSchema],
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_data: UserCreateSchema, session: AsyncSession = Depends(get_session)
):
    result = await user_service.create_user(user_data, session)
    return ResponseSchema(detail="Success", result=result)


@auth_router.post("/login")
async def login_user(
    login_data: UserLoginSchema, session: AsyncSession = Depends(get_session)
):
    user = await user_service.login_user(login_data, session)

    access_token = create_access_token(str(user.uid))
    return JSONResponse(
        content={
            "message": "Login successful",
            "access_token": access_token,
            "token_type": "Bearer",
            "user": {
                "user_uid": str(user.uid),
                "email": user.email,
                "username": user.username,
            },
        }
    )


@auth_router.get("/me", response_model=ResponseSchema[UserSchema])
async def get_current_user_info(
    current_user: UserLoginSchema = Depends(get_current_user),
):
    return ResponseSchema(detail="Success", result=current_user)


@auth_router.get("/all", response_model=ResponseSchema[PageResponse[UserSchema]])
async def get_all_users(
    session: AsyncSession = Depends(get_session),
    page: int | None = 1,
    limit: int | None = 10,
):
    result = await user_service.get_all_users(session, page, limit)
    return ResponseSchema(detail="Success", result=result)


@auth_router.get("/{user_uid}", response_model=ResponseSchema[UserSchema])
async def get_user_by_uid(
    user_uid: str, session: AsyncSession = Depends(get_session)
) -> dict:
    result = await user_service.get_user_by_uid(user_uid, session)
    return ResponseSchema(detail="Success", result=result)


@auth_router.patch("/{user_uid}", response_model=ResponseSchema[UserSchema])
async def update_user(
    user_uid: str,
    user_update_data: UserUpdateSchema,
    session: AsyncSession = Depends(get_session),
) -> dict:
    result = await user_service.update_user(user_uid, user_update_data, session)
    return ResponseSchema(detail="Success", result=result)


@auth_router.delete("/{user_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_uid(
    user_uid: str, session: AsyncSession = Depends(get_session)
):
    await user_service.delete_user(user_uid, session)
    return {}


REFRESH_TOKEN_EXPIRY = 2
