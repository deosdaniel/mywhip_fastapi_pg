from src.utils.base_service_repo import BaseRepository


class AuthRepository(BaseRepository):
    async def authenticate(self, username, password):
        pass
