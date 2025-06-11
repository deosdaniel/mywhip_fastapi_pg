import asyncio

from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.core import engine
from src.users.repositories import UsersRepository
from src.users.schemas import UserCreateSchema
from src.users.service import UserService
from src.cars.models import Cars
from src.users.models import Users


async def create_admin():
    async with AsyncSession(engine) as session:
        user_repository = UsersRepository(session)
        user_service = UserService(user_repository)
        admin_data = UserCreateSchema(
            username="super_user",
            email="admin@admin.com",
            password="admin123",
            first_name="super",
            last_name="user",
        )
        try:
            await user_service.create_admin(admin_data)
            print("Admin created successfully")
        except HTTPException as e:
            print(f"Failed: {e}")


if __name__ == "__main__":
    asyncio.run(create_admin())
