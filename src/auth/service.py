import math
from fastapi.exceptions import HTTPException
from fastapi import status
from sqlalchemy import func
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from .utils import gen_pwd_hash, verify_pwd
from .models import Users
from .schemas import UserCreateSchema, UserUpdateSchema, PageResponse, UserLoginSchema
from src.utils.exceptions import EntityNotFoundException


class UserService:
    async def login_user(self, login_data: UserLoginSchema, session: AsyncSession):
        exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid email or pwd"
        )
        check_user = await session.exec(
            select(Users).where(Users.email == login_data.email)
        )
        user = check_user.first()
        if not user:
            raise exc
        if not verify_pwd(login_data.password, user.password_hash):
            raise exc
        return user

    async def get_user_by_uid(self, user_uid: str, session: AsyncSession):
        statement = select(Users).where(Users.uid == user_uid)
        result = await session.exec(statement)
        user = result.first()
        if user:
            return user
        else:
            raise EntityNotFoundException("user_uid")

    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(Users).where(Users.email == email)
        result = await session.exec(statement)
        result = result.first()
        if result:
            return result
        else:
            raise EntityNotFoundException("Email")

    async def get_all_users(self, session: AsyncSession, page: int, limit: int):
        statement = select(Users).order_by(desc(Users.created_at))
        # Pagination
        offset_page = page - 1
        statement = statement.offset(offset_page * limit).limit(limit)
        # Counting records, pages
        count_statement = select(func.count(1)).select_from(Users)
        total_records = (await session.exec(count_statement)).one() or 0
        total_pages = math.ceil(total_records / limit)
        # Executing query
        result = await session.exec(statement)
        result = result.all()
        return PageResponse(
            page_number=page,
            page_size=limit,
            total_pages=total_pages,
            total_records=total_records,
            content=result,
        )

    async def email_exists(self, email: str, session: AsyncSession):
        statement = select(Users).where(Users.email == email)
        result = await session.exec(statement)
        user = result.first()
        return True if user else False

    async def username_exists(self, username: str, session: AsyncSession):
        statement = select(Users).where(Users.username == username)
        result = await session.exec(statement)
        user = result.first()
        return True if user else False

    async def create_user(self, user_data: UserCreateSchema, session: AsyncSession):
        email_exists = await self.email_exists(user_data.email, session)
        username_exists = await self.username_exists(user_data.username, session)
        if not email_exists and not username_exists:
            user_data_dict = user_data.model_dump()
            new_user = Users(**user_data_dict)
            new_user.password_hash = gen_pwd_hash(user_data_dict["password"])
            session.add(new_user)
            await session.commit()
            return new_user
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User with this email or username already exists",
            )

    async def update_user(
        self, user_uid: str, update_data: UserUpdateSchema, session: AsyncSession
    ):
        user_to_update = await self.get_user_by_uid(user_uid, session)
        update_data_dict = update_data.model_dump()
        for k, v in update_data_dict.items():
            setattr(user_to_update, k, v)
        await session.commit()
        await session.refresh(user_to_update)
        return user_to_update

    async def delete_user(self, user_uid: str, session: AsyncSession):
        user_to_delete = await self.get_user_by_uid(user_uid, session)
        await session.delete(user_to_delete)
        await session.commit()
        return True
