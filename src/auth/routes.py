from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse
from src.auth.utils import create_access_token
from src.auth.service import AuthService
from src.users.schemas import UserSchema
from src.auth.schemas import AuthSchema
from src.auth.dependencies import get_auth_service, get_current_user

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


@auth_router.get("/me")
async def get_current_user_info(
    current_user: AuthSchema = Depends(get_current_user),
) -> UserSchema:
    return current_user
