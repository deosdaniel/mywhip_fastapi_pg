import math
from fastapi.exceptions import HTTPException
from fastapi import status
from sqlalchemy import func

from sqlmodel import select, desc
from .models import Users
from src.utils.schemas_common import PageResponse
from .schemas import UserCreateSchema, UserUpdateSchema
from src.auth.utils import gen_pwd_hash

from ..utils.exceptions import EntityNotFoundException

from src.utils.base_service import BaseService


class UserService(BaseService):

    async def create_user(self, user_data: UserCreateSchema):
        email_exists = await self.email_exists(user_data.email)
        username_exists = await self.username_exists(user_data.username)
        if not email_exists and not username_exists:
            user_data_dict = user_data.model_dump()
            new_user = Users(**user_data_dict)
            new_user.password_hash = gen_pwd_hash(user_data_dict["password"])
            self.session.add(new_user)
            await self.session.commit()
            return new_user
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User with this email or username already exists",
            )

    async def get_user_by_uid(self, user_uid: str):
        statement = select(Users).where(Users.uid == user_uid)
        result = await self.session.exec(statement)
        user = result.first()
        if user:
            return user
        else:
            return None

    async def get_user_by_email(self, email: str):
        statement = select(Users).where(Users.email == email)
        result = await self.session.exec(statement)
        result = result.first()
        if result:
            return result
        else:
            return None

    async def get_all_users(self, page: int, limit: int):
        statement = select(Users).order_by(desc(Users.created_at))
        # Pagination
        offset_page = page - 1
        statement = statement.offset(offset_page * limit).limit(limit)
        # Counting records, pages
        count_statement = select(func.count(1)).select_from(Users)
        total_records = (await self.session.exec(count_statement)).one() or 0
        total_pages = math.ceil(total_records / limit)
        # Executing query
        result = await self.session.exec(statement)
        result = result.all()
        return PageResponse(
            page_number=page,
            page_size=limit,
            total_pages=total_pages,
            total_records=total_records,
            content=result,
        )

    async def email_exists(self, email: str):
        statement = select(Users).where(Users.email == email)
        result = await self.session.exec(statement)
        user = result.first()
        return True if user else False

    async def username_exists(self, username: str):
        statement = select(Users).where(Users.username == username)
        result = await self.session.exec(statement)
        user = result.first()
        return True if user else False

    async def update_user(self, user_uid: str, update_data: UserUpdateSchema):
        user_to_update = await self.get_user_by_uid(user_uid)
        if user_to_update:
            update_data_dict = update_data.model_dump()
            for k, v in update_data_dict.items():
                setattr(user_to_update, k, v)
            await self.session.commit()
            await self.session.refresh(user_to_update)
            return user_to_update
        else:
            raise EntityNotFoundException("user_uid")

    async def delete_user(self, user_uid: str):
        user_to_delete = await self.get_user_by_uid(user_uid)
        if user_to_delete:
            await self.session.delete(user_to_delete)
            await self.session.commit()
            return True
        else:
            raise EntityNotFoundException("user_uid")
