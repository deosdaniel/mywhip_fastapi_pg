from fastapi.exceptions import HTTPException
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.users.service import UserService
from src.auth.utils import verify_pwd


class AuthService:
    async def authenticate_user(self, email: str, password: str, session: AsyncSession):
        exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid email or pwd"
        )
        check_user = UserService()
        user = await check_user.get_user_by_email(email, session)
        if not user:
            raise exc
        if not verify_pwd(password, user.password_hash):
            raise exc
        return user
