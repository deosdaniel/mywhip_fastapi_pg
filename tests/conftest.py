import os
import uuid
import pytest
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient, ASGITransport
import pandas as pd
from src.directories.models import MakesDirectory, ModelsDirectory
from src.main import app
from src.db.core import get_session
from src.users.schemas import UserSchema, UserRole
from src.auth.dependencies import get_current_user


DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine_test = create_async_engine(DATABASE_URL, echo=False)
TestSession = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)


# ✅ Создание и удаление таблиц один раз за сессию
@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


# ✅ Очистка данных после каждого теста
@pytest.fixture(scope="function", autouse=True)
async def clean_database():
    # После каждого теста удаляем все записи из всех таблиц
    yield
    async with engine_test.begin() as conn:
        for table in reversed(SQLModel.metadata.sorted_tables):
            if table.name not in {"makesdir", "modelsdir"}:
                await conn.execute(table.delete())


@pytest.fixture(scope="function", autouse=True)
async def test_session():
    async def override_get_session():
        async with TestSession() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    yield
    app.dependency_overrides.pop(get_session, None)


@pytest.fixture(scope="function", autouse=True)
async def client(test_session):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


# --- Новые общие фикстуры: ---


# auth router
@pytest.fixture
def create_user(
    client,
):  # для создания реального пользователя с токеном через /signup
    async def _create(username: str, email: str, password="securepassword"):
        response = await client.post(
            "/api/v1/users/signup",
            json={
                "username": username,
                "email": email,
                "first_name": "Test",
                "last_name": "User",
                "password": password,
            },
        )
        assert response.status_code == 201
        return response.json()["result"]

    return _create


@pytest.fixture
def get_access_token(
    client, create_user
):  # Создать пользователя функцией выше и залогиниться
    async def _get(email="authuser@example.com", password="securepassword"):
        username = email.split("@")[0]
        await create_user(username, email, password)
        response = await client.post(
            "/api/v1/auth/login",
            data={"username": email, "password": password},
        )
        assert response.status_code == 200
        return response.json()["access_token"]

    return _get


# user-router
@pytest.fixture
def mock_user_factory():  # для подмены в защищенных эндпоинтах
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


# справочники
@pytest.fixture(scope="session", autouse=True)
async def load_directories(prepare_database):
    BASE_DIR = os.path.dirname(__file__)
    csv_path = os.path.join(BASE_DIR, "../src/directories/make_model_dataset.csv")
    df = pd.read_csv(csv_path)
    df_makes = (
        df.drop("model", axis=1).drop_duplicates(subset="make").reset_index(drop=True)
    )

    async with TestSession() as session:
        # Добавляем марки с явным UUID, генерируемым в Python
        make_map = {}
        for _, row in df_makes.iterrows():
            make_obj = MakesDirectory(
                uid=uuid.uuid4(),  # вот тут создаём UUID вручную
                make=row["make"],
            )
            session.add(make_obj)
            await session.flush()  # нужно, чтобы получить uid сразу после добавления
            make_map[row["make"]] = make_obj.uid

        # Добавляем модели с явным UUID
        for _, row in df.iterrows():
            model_obj = ModelsDirectory(
                uid=uuid.uuid4(),  # также явно задаём UUID для моделей
                model=row["model"],
                make_uid=make_map[row["make"]],
            )
            session.add(model_obj)

        await session.commit()
