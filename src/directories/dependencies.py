from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends

from ..db.core import get_session
from .service import DirectoryService


def get_dir_service(session: AsyncSession = Depends(get_session)) -> DirectoryService:
    return DirectoryService(session)
