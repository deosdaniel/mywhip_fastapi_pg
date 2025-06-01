from fastapi.exceptions import HTTPException
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from .utils import generate_pwd_hash

from .models import Users
from .schemas import UserCreateSchema, UserUpdateSchema


def raise_item_not_found_exception(item: str):
    return HTTPException(
        status_code=404, detail=f"Sorry, requested {item}_uid does not exist"
    )


class UserService:
    async def get_user_by_uid(self, user_uid: str, session: AsyncSession):
        statement = select(Users).where(Users.uid == user_uid)
        result = await session.exec(statement)
        user = result.first()
        if user:
            return user
        else:
            return raise_item_not_found_exception("user")

    async def get_all_users(self, session: AsyncSession):
        statement = select(Users).order_by(desc(Users.created_at))
        result = await session.exec(statement)
        return result.all()

    async def email_exists(self, email: str, session: AsyncSession):
        statement = select(Users).where(Users.email == email)
        result = await session.exec(statement)
        user = result.first()
        return True if user else False

    async def create_user(self, user_data: UserCreateSchema, session: AsyncSession):
        email_exists = await self.email_exists(user_data.email, session)
        if not email_exists:
            user_data_dict = user_data.model_dump()
            new_user = Users(**user_data_dict)
            new_user.password_hash = generate_pwd_hash(user_data_dict["password"])
            session.add(new_user)
            await session.commit()
            return new_user
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User with this email already exists",
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
