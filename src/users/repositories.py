from sqlmodel import select
from src.users.models import Users
from src.utils.base_service_repo import BaseRepository


class UsersRepository(BaseRepository):

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
