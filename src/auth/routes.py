from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse


from src.auth.utils import create_access_token
from src.db.main import db_session
from src.auth.service import AuthService

auth_router = APIRouter()

auth_service = AuthService()


@auth_router.post("/login")
async def authenticate_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: db_session,
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
