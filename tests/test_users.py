import pytest
from httpx import AsyncClient

# Данные для создания пользователя
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
    assert response.status_code == 201, f"Unexpected: {response.text}"

    data = response.json()
    assert data["detail"] == "Success"
    assert data["result"]["username"] == user_data["username"]


@pytest.mark.asyncio
async def test_get_user_by_uid(client: AsyncClient):
    # Создаём пользователя
    response = await client.post(
        "/api/v1/users/signup",
        json={
            "username": "uidtester",
            "email": "uidtester@example.com",
            "first_name": "Uid",
            "last_name": "Tester",
            "password": "securepassword",
        },
    )
    assert response.status_code == 201
    uid = response.json()["result"]["uid"]

    # Получаем его по uid
    get_response = await client.get(f"/api/v1/users/{uid}")
    assert get_response.status_code == 200
    assert get_response.json()["result"]["uid"] == uid


@pytest.mark.asyncio
async def test_get_all_users(client: AsyncClient):
    response = await client.get("/api/v1/users/all")
    assert response.status_code == 200
    users = response.json()["result"]["content"]
    assert isinstance(users, list)
