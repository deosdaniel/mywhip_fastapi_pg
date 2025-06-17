import uuid
import pytest
from httpx import AsyncClient, ASGITransport
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.db.core import get_session
from src.auth.dependencies import require_admin, require_self_or_admin
from src.users.schemas import UserSchema, UserRole

# Используем SQLite in-memory
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine_test = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSession = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)


# Создание и удаление таблиц
@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


# Мокаем авторизованного пользователя (админа)
mock_admin = UserSchema(
    uid=uuid.uuid4(),
    role=UserRole.ADMIN,
    username="mockadmin",
    email="mock@admin.com",
    first_name="Mock",
    last_name="Admin",
    is_verified=True,
    password_hash="",
    created_at=None,
    updated_at=None,
)

mock_user = UserSchema(
    uid=uuid.uuid4(),
    role=UserRole.USER,
    username="mockuser",
    email="mock@example.com",
    first_name="Mock",
    last_name="User",
    is_verified=True,
    password_hash="",
    created_at=None,
    updated_at=None,
)


# Подменяем зависимости авторизации
app.dependency_overrides[require_admin] = lambda: mock_admin
app.dependency_overrides[require_self_or_admin] = lambda: mock_user


# Фикстура клиента
@pytest.fixture
async def client():
    async def override_get_session():
        async with TestSession() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
