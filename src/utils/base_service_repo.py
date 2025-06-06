from sqlmodel.ext.asyncio.session import AsyncSession

from typing import TypeVar, Generic


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


R = TypeVar("R", bound=BaseRepository)


class BaseService(Generic[R]):
    def __init__(self, repository: R):
        self.repository: R = repository
