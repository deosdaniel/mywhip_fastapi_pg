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
async def test_create_user_success(client: AsyncClient):
    response = await client.post("/api/v1/users/signup", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["result"]["username"] == user_data["username"]


@pytest.mark.asyncio
async def test_create_user_conflict_email(client: AsyncClient):
    bad_data = {**user_data, "username": "testuser123"}
    response = await client.post("/api/v1/users/signup", json=bad_data)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_create_user_conflict_username(client: AsyncClient):
    bad_data = {**user_data, "email": "example@test123.com"}
    response = await client.post("/api/v1/users/signup", json=bad_data)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_create_user_short_username(client: AsyncClient):
    bad_data = {**user_data, "username": "abc"}
    response = await client.post("/api/v1/users/signup", json=bad_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_user_short_password(client: AsyncClient):
    bad_data = {**user_data, "password": "abc123"}
    response = await client.post("/api/v1/users/signup", json=bad_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_user_invalid_email(client: AsyncClient):
    bad_data = {**user_data, "email": "testexample.com"}
    response = await client.post("/api/v1/users/signup", json=bad_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_user_invalid_password(client: AsyncClient):
    bad_data = {**user_data, "password": "abc123"}
    response = await client.post("/api/v1/users/signup", json=bad_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_user_empty_input(client: AsyncClient):
    bad_data = {}
    response = await client.post("/api/v1/users/signup", json=bad_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_explicit_admin_role_fail(client: AsyncClient):
    response = await client.post(
        "/api/v1/users/signup",
        json={
            "username": "hacker",
            "email": "evil@hacker.com",
            "password": "supersecure",
            "first_name": "E",
            "last_name": "Hacker",
            "role": "admin",
        },
    )
    assert response.status_code == 422


@pytest.mark.parametrize(
    "role,expected_status",
    [
        (UserRole.ADMIN, 200),
        (UserRole.USER, 403),
    ],
)
@pytest.mark.asyncio
async def test_get_all_users_by_role(
    client, mock_user_factory, override_current_user, role, expected_status
):
    mock_user = mock_user_factory(role)
    override_current_user(mock_user)
    response = await client.get("/api/v1/users/all")
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "actor_role,is_self,expected_status",
    [
        (UserRole.ADMIN, False, 200),
        (UserRole.USER, True, 200),
        (UserRole.USER, False, 403),
    ],
)
@pytest.mark.asyncio
async def test_user_access_by_role_and_ownership(
    client,
    mock_user_factory,
    override_current_user,
    actor_role,
    is_self,
    expected_status,
):
    target_username = f"target_{uuid.uuid4().hex[:6]}"
    target_email = f"{target_username}@example.com"

    # создаём пользователя
    response = await client.post(
        "/api/v1/users/signup",
        json={
            "username": target_username,
            "email": target_email,
            "first_name": "Target",
            "last_name": "User",
            "password": "securepassword",
        },
    )
    assert response.status_code == 201
    target_uid = response.json()["result"]["uid"]

    # подставляем mock-пользователя
    uid = uuid.UUID(target_uid) if is_self else uuid.uuid4()
    mock_user = mock_user_factory(actor_role, uid=uid)
    override_current_user(mock_user)

    response = await client.get(f"/api/v1/users/{target_uid}")
    assert response.status_code == expected_status
