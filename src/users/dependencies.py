from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends

from ..db.main import get_session
from .service import UserService


def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(session)
