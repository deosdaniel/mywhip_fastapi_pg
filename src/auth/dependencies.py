from typing import Annotated
from fastapi import Depends, HTTPException, status

from src.auth.service import AuthService
from src.users.dependencies import get_user_service
from src.users.models import Users
from src.users.schemas import UserSchema, UserRole
from src.users.service import UserService
from fastapi.security import OAuth2PasswordBearer
from src.auth.utils import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: UserService = Depends(get_user_service),
) -> UserSchema:

    token_data = decode_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalid or expired"
        )
    user = await user_service.get_by_uid(table=Users, uid=token_data["sub"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user


async def check_admin_privileges(
    current_user: UserSchema = Depends(get_current_user),
) -> UserSchema:
    if not current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action",
        )
    return current_user


def get_auth_service(
    user_service: UserService = Depends(get_user_service),
) -> AuthService:
    return AuthService(user_service)
