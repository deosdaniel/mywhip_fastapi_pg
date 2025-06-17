import uuid
import pytest
from httpx import AsyncClient
from src.users.schemas import UserSchema, UserRole
from src.auth.dependencies import get_current_user  # ✅ Переопределяем именно это
from src.main import app


# Общие данные для создания пользователя
user_data = {
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "securepassword",
}


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post("/api/v1/users/signup", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["result"]["username"] == user_data["username"]


@pytest.mark.parametrize(
    "role,expected_status",
    [
        (UserRole.ADMIN, 200),
        (UserRole.USER, 403),
    ],
)
@pytest.mark.asyncio
async def test_get_all_users_by_role(client: AsyncClient, role, expected_status):
    # Создаём mock-пользователя с нужной ролью
    mock_user = UserSchema(
        uid=uuid.uuid4(),
        role=role,
        username=f"{role}_mock",
        email=f"{role}@test.com",
        first_name="Mock",
        last_name="User",
        is_verified=True,
        password_hash="",
        created_at=None,
        updated_at=None,
    )

    # ✅ Переопределяем get_current_user, а не require_admin
    app.dependency_overrides[get_current_user] = lambda: mock_user

    response = await client.get("/api/v1/users/all")
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "role,expected_status",
    [
        (UserRole.ADMIN, 200),
        (UserRole.USER, 200),
    ],
)
@pytest.mark.asyncio
async def test_get_user_by_uid_with_roles(client: AsyncClient, role, expected_status):
    # Сначала создаём пользователя через /signup
    create_response = await client.post(
        "/api/v1/users/signup",
        json={
            "username": f"user_{role}",
            "email": f"{role}@test.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "securepassword",
        },
    )
    assert create_response.status_code == 201
    uid = create_response.json()["result"]["uid"]

    # Создаём mock-пользователя, представляющего "себя" или админа
    mock_user = UserSchema(
        uid=uuid.UUID(uid),
        role=role,
        username=f"{role}_mock",
        email=f"{role}@test.com",
        first_name="Mock",
        last_name="User",
        is_verified=True,
        password_hash="",
        created_at=None,
        updated_at=None,
    )

    app.dependency_overrides[get_current_user] = lambda: mock_user

    response = await client.get(f"/api/v1/users/{uid}")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json()["result"]["uid"] == uid
