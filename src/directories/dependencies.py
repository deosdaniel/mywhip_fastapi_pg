from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends

from ..db.core import get_session
from .service import DirectoryService
from .repositories import DirectoryRepository


def get_dir_repository(
    session: AsyncSession = Depends(get_session),
) -> DirectoryRepository:
    return DirectoryRepository(session)


def get_dir_service(
    repository: DirectoryRepository = Depends(get_dir_repository),
) -> DirectoryService:
    return DirectoryService(repository)
