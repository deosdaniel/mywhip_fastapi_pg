from fastapi.exceptions import HTTPException
from fastapi import status

from src.users.service import UserService
from src.auth.utils import verify_pwd
from src.utils.base_service_repo import BaseService


class AuthService(BaseService):
    async def authenticate_user(self, email: str, password: str):
        exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid email or pwd"
        )
        check_user = UserService(self.session)
        user = await check_user.get_user_by_email(email)
        if not user:
            raise exc
        if not verify_pwd(password, user.password_hash):
            raise exc
        return user
