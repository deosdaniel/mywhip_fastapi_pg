from fastapi.exceptions import HTTPException
from fastapi import status
from src.users.service import UserService
from src.auth.utils import verify_pwd
from src.utils.base_service_repo import BaseService


class AuthService(BaseService):
    def __init__(self, user_service: UserService):
        super().__init__(user_service)
        self.user_service = user_service

    async def authenticate_user(self, email: str, password: str):
        exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid email or pwd"
        )
        user = await self.user_service.get_user_by_email(email)
        if not user:
            raise exc
        if not verify_pwd(password, user.password_hash):
            raise exc
        return user
