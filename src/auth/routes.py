from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependencies import get_auth_service
from src.auth.utils import create_access_token
from src.auth.service import AuthService

auth_router = APIRouter()


@auth_router.post("/login")
async def authenticate_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthService = Depends(get_auth_service),
):
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
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
