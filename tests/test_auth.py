import pytest


@pytest.mark.asyncio
async def test_auth_login_success(client, create_user):
    await create_user("loginuser", "login@user.com")
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "login@user.com", "password": "securepassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["username"] == "loginuser"


@pytest.mark.asyncio
async def test_auth_login_invalid_password(client, create_user):
    await create_user("loginuser", "login@user.com")
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "loginuser", "password": "securepassword123"},
    )
    assert response.status_code == 401
    assert "invalid email or pwd" in response.text


@pytest.mark.asyncio
async def test_auth_login_nonexistent_user(client, create_user):
    await create_user("loginuser", "login@user.com")
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "loginuser123", "password": "securepassword"},
    )
    assert response.status_code == 401
    assert "invalid email or pwd" in response.text


@pytest.mark.asyncio
async def test_auth_validate_token_success(client, get_access_token):
    token = await get_access_token()
    response = await client.get(
        "/api/v1/auth/validate",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Token verified"


@pytest.mark.asyncio
async def test_auth_validate_missing_token(client):
    response = await client.get(
        "/api/v1/auth/validate",
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_auth_validate_invalid_token(client):
    response = await client.get(
        "/api/v1/auth/validate",
        headers={"Authorization": "Bearer qwerty.asdf.zxcv"},
    )
    assert response.status_code == 401
    assert "Token invalid or expired" in response.text


@pytest.mark.asyncio
async def test_auth_get_me_info_success(client, get_access_token):
    token = await get_access_token()
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "authuser@example.com"
    assert data["username"] == "authuser"


@pytest.mark.asyncio
async def test_auth_get_me_info_no_token(client):
    response = await client.get("api/v1/auth/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_auth_get_me_info_invalid_token(client):
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer qwerty.asdf.zxcv"},
    )
    assert response.status_code == 401
