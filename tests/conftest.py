from typing import AsyncGenerator


from fastapi.testclient import TestClient
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from src.config import Config
from src.db.main import get_session
from src.main import app
import pytest_asyncio

DB_URL = Config.TEST_DATABASE_URL


test_engine = create_async_engine(url=DB_URL, echo=True)


async def test_get_session() -> AsyncGenerator[AsyncSession, None]:
    test_session = sessionmaker(
        bind=test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with test_session() as session:
        yield session


@pytest_asyncio.fixture(scope="session")
async def test_client() -> TestClient:
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

        app.dependency_overrides[get_session] = test_get_session

    with TestClient(app) as client:
        yield client
