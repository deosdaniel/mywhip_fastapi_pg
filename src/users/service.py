import math
from fastapi.exceptions import HTTPException
from fastapi import status
from src.utils.schemas_common import PageResponse
from .repositories import UsersRepository
from .schemas import UserCreateSchema, UserUpdateSchema
from ..auth.utils import gen_pwd_hash

from ..utils.exceptions import EntityNotFoundException

from src.utils.base_service_repo import BaseService


class UserService(BaseService[UsersRepository]):

    async def create_user(self, user_data: UserCreateSchema):
        email_exists = await self.get_user_by_email(user_data.email)
        username_exists = await self.get_user_by_username(user_data.username)
        if not email_exists and not username_exists:
            user_dict = user_data.model_dump()
            user_dict["password_hash"] = gen_pwd_hash(user_data.password)
            return await self.repository.create_user(user_dict)
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User with this email or username already exists",
            )

    async def get_user_by_uid(self, user_uid: str):
        user = await self.repository.get_user_by_uid(user_uid)
        if user:
            return user
        else:
            return None

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

    async def get_all_users(self, page: int, limit: int):

        offset_page = (page - 1) * limit

        users = await self.repository.get_all_users(offset_page, limit)

        total_records = await self.repository.count_all_records()
        total_pages = math.ceil(total_records / limit)

        return PageResponse(
            page_number=page,
            page_size=limit,
            total_pages=total_pages,
            total_records=total_records,
            content=users,
        )

    async def update_user(self, user_uid: str, update_data: UserUpdateSchema):
        update_dict = update_data.model_dump(exclude_unset=True)
        updated_user = await self.repository.update_user(user_uid, update_dict)
        if not updated_user:
            raise EntityNotFoundException("user_uid")
        return updated_user

    async def delete_user(self, user_uid: str):
        delete_user = await self.repository.delete_user(user_uid)
        if delete_user:
            return True
        else:
            raise EntityNotFoundException("user_uid")
