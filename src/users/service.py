from fastapi.exceptions import HTTPException
from fastapi import status

from .models import Users
from .repositories import UsersRepository
from .schemas import UserCreateSchema
from ..auth.utils import gen_pwd_hash


from src.utils.base_service_repo import BaseService


class UserService(BaseService[UsersRepository]):

    async def create_user(self, user_data: UserCreateSchema):
        email_exists = await self.get_user_by_email(user_data.email)
        username_exists = await self.get_user_by_username(user_data.username)
        if not email_exists and not username_exists:
            user_dict = user_data.model_dump()
            user_dict["password_hash"] = gen_pwd_hash(user_data.password)
            return await self.repository.create(table=Users, new_entity_dict=user_dict)
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User with this email or username already exists",
            )

    async def get_user_by_email(self, email: str):
        user = await self.repository.get_user_by_email(email)
        if user:
            return user
        else:
            return None

    async def get_user_by_username(self, username: str):
        user = await self.repository.get_user_by_username(username)
        if user:
            return user
        else:
            return None
