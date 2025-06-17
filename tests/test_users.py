import uuid
import pytest
from httpx import AsyncClient
from src.users.schemas import UserRole


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
    await client.post(
        "/api/v1/users/signup",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "securepassword",
        },
    )
    response = await client.post(
        "/api/v1/users/signup",
        json={
            "username": "testuser123",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "securepassword",
        },
    )
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_user_conflict_username(client: AsyncClient):
    await client.post(
        "/api/v1/users/signup",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "securepassword",
        },
    )
    response = await client.post(
        "/api/v1/users/signup",
        json={
            "username": "testuser",
            "email": "test123@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "securepassword",
        },
    )
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


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
async def test_get_all_users_role(
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
async def test_get_user_by_uid_role_and_ownership(
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


@pytest.mark.parametrize(
    "actor_role,is_self, expected_status",
    [
        (UserRole.ADMIN, False, 200),
        (UserRole.USER, True, 200),
        (UserRole.USER, False, 403),
    ],
)
@pytest.mark.asyncio
async def test_update_user_by_uid_role_and_ownership(
    client,
    mock_user_factory,
    override_current_user,
    actor_role,
    is_self,
    expected_status,
):
    # создадим пользователя
    response = await client.post(
        "/api/v1/users/signup",
        json={
            "username": "update_target",
            "email": "update@target.com",
            "first_name": "Old",
            "last_name": "Oldest",
            "password": "securepassword",
        },
    )

    assert response.status_code == 201
    user_uid = response.json()["result"]["uid"]

    # создадим того, что будет производить действие (обновлять данные)
    uid = uuid.UUID(user_uid) if is_self else uuid.uuid4()
    mock_user = mock_user_factory(actor_role, uid=uid)
    override_current_user(mock_user)

    # обновляем данные
    response = await client.patch(
        f"/api/v1/users/{user_uid}",
        json={"first_name": "New", "last_name": "Newest"},
    )
    assert response.status_code == expected_status

    if expected_status == 200:
        assert response.json()["result"]["first_name"] == "New"


@pytest.mark.parametrize(
    "actor_role, is_self, expected_status",
    [
        (UserRole.ADMIN, False, 204),
        (UserRole.USER, True, 204),
        (UserRole.USER, False, 403),
    ],
)
@pytest.mark.asyncio
async def test_delete_user_by_uid_role_and_ownership(
    client,
    mock_user_factory,
    override_current_user,
    actor_role,
    is_self,
    expected_status,
):
    response = await client.post(
        "/api/v1/users/signup",
        json={
            "username": "delete_target",
            "email": "delete@target.com",
            "first_name": "Delete",
            "last_name": "User",
            "password": "securepassword",
        },
    )
    assert response.status_code == 201
    user_uid = response.json()["result"]["uid"]

    uid = uuid.UUID(user_uid) if is_self else uuid.uuid4()
    mock_user = mock_user_factory(actor_role, uid=uid)
    override_current_user(mock_user)

    response = await client.delete(f"/api/v1/users/{user_uid}")
    assert response.status_code == expected_status
    if expected_status == 204:
        override_current_user(mock_user_factory(UserRole.ADMIN))
        response = await client.get(f"/api/v1/users/{user_uid}")
        assert response.status_code == 404
