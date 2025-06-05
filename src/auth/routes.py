from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession


from src.auth.utils import create_access_token
from src.db.main import get_session
from src.auth.service import AuthService

auth_router = APIRouter()

auth_service = AuthService()


@auth_router.post("/login")
async def authenticate_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_session),
):
    user = await auth_service.authenticate_user(
        form_data.username, form_data.password, session
    )
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
