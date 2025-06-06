from pydantic_core.core_schema import none_schema
from sqlalchemy import desc, func
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc

from src.auth.utils import gen_pwd_hash
from src.users.models import Users
from src.users.schemas import UserUpdateSchema, UserCreateSchema
from src.utils.base_service_repo import BaseRepository


class UsersRepository(BaseRepository):

    async def create_user(self, user_data: UserCreateSchema) -> Users:
        user_dict = user_data.model_dump()
        user = Users(**user_dict)
        user.password_hash = gen_pwd_hash(user_dict["password"])
        self.session.add(user)
        await self.session.commit()
        return user

    async def get_user_by_uid(self, requested_uid: str) -> Users:
        user = await self.session.exec(select(Users).where(Users.uid == requested_uid))
        return user.one_or_none()

    async def get_user_by_email(self, requested_email: str) -> Users:
        user = await self.session.exec(
            select(Users).where(Users.email == requested_email)
        )
        return user.one_or_none()

    async def get_user_by_username(self, requested_name: str) -> Users:
        user = await self.session.exec(
            select(Users).where(Users.username == requested_name)
        )
        return user.one_or_none()

    async def get_all_users(self, offset_page: int, limit: int) -> list[Users]:
        statement = (
            select(Users)
            .offset(offset_page)
            .limit(limit)
            .order_by(desc(Users.created_at))
        )

        users = await self.session.exec(statement)
        return users

    async def count_all_records(self):
        result = await self.session.exec(select(func.count(Users.uid)))
        return result.one()

    async def update_user(self, user_uid: str, update_data: UserUpdateSchema) -> Users:
        user_to_update = await self.get_user_by_uid(user_uid)
        if user_to_update:
            update_data_dict = update_data.model_dump()
            for k, v in update_data_dict.items():
                setattr(user_to_update, k, v)
            await self.session.commit()
            await self.session.refresh(user_to_update)
            return user_to_update
        else:
            return None

    async def delete_user(self, user_uid: str):
        user_to_delete = await self.get_user_by_uid(user_uid)
        if user_to_delete:
            await self.session.delete(user_to_delete)
            await self.session.commit()
            return True
        else:
            return False
