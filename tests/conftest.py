import uuid

import pytest
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from httpx import AsyncClient, ASGITransport

from src.auth.dependencies import get_current_user
from src.main import app
from src.db.core import get_session
from src.users.schemas import UserSchema, UserRole

DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine_test = create_async_engine(DATABASE_URL, echo=False)
TestSession = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture
async def test_session():
    async def override_get_session():
        async with TestSession() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    yield
    app.dependency_overrides.pop(get_session, None)


@pytest.fixture
async def client(test_session):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


# --- Новые общие фикстуры: ---


@pytest.fixture
def mock_user_factory():
    def _create(role: UserRole, uid: uuid.UUID = None) -> UserSchema:
        return UserSchema(
            uid=uid or uuid.uuid4(),
            role=role,
            username=f"{role}_mock",
            email=f"{role}_mock@example.com",
            first_name="Mock",
            last_name="User",
            is_verified=True,
            password_hash="",
            created_at=None,
            updated_at=None,
        )

    return _create


@pytest.fixture
def override_current_user():
    def _override(user: UserSchema):
        app.dependency_overrides[get_current_user] = lambda: user

    yield _override
    app.dependency_overrides.pop(get_current_user, None)
