from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends

from .repositories import UsersRepository
from ..db.core import get_session
from .service import UserService


def get_user_repository(
    session: AsyncSession = Depends(get_session),
) -> UsersRepository:
    return UsersRepository(session)


def get_user_service(
    repository: UsersRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repository)
