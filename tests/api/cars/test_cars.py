import pytest
from src.users.schemas import UserRole
from tests.api.cars.cars_helpers import create_mock_car, create_five_mock_cars
from tests.conftest import mock_user_factory, override_current_user


@pytest.fixture()
def mock_car_single():
    return {
        "make": "Toyota",
        "model": "Corolla",
        "year": 2005,
        "vin": "JZX10012345678901",
        "pts_num": "55ХВ123123",
        "sts_num": "9955123123",
        "date_purchased": "2025-06-18",
        "price_purchased": 250000,
        "status": "FRESH",
    }


@pytest.fixture
def mock_cars():
    return [
        {
            "make": "Toyota",
            "model": "Corolla",
            "year": 2005,
            "vin": "JZX10012345678901",
            "pts_num": "55ХВ123123",
            "sts_num": "9955123123",
            "date_purchased": "2025-06-18",
            "price_purchased": 250000,
            "status": "FRESH",
        },
        {
            "make": "Honda",
            "model": "Accord",
            "year": 2002,
            "vin": "JZX10012345678902",
            "pts_num": "55ХВ123123",
            "sts_num": "9955123123",
            "date_purchased": "2025-06-17",
            "price_purchased": 750000,
            "status": "FRESH",
        },
        {
            "make": "Mitsubishi",
            "model": "Lancer",
            "year": 2007,
            "vin": "JZX10012345678903",
            "pts_num": "55ХВ123123",
            "sts_num": "9955123123",
            "date_purchased": "2025-06-14",
            "price_purchased": 420000,
            "status": "FRESH",
        },
        {
            "make": "Nissan",
            "model": "Juke",
            "year": 2017,
            "vin": "JZX10012345678923",
            "pts_num": "55ХВ123123",
            "sts_num": "9955123123",
            "date_purchased": "2025-06-11",
            "price_purchased": 67200,
            "status": "FRESH",
        },
        {
            "make": "Opel",
            "model": "Astra",
            "year": 2012,
            "vin": "JZX10012348678923",
            "pts_num": "55ХВ123123",
            "sts_num": "9955123123",
            "date_purchased": "2025-06-11",
            "price_purchased": 524000,
            "status": "FRESH",
        },
    ]


@pytest.fixture()
def mock_car_update():
    return {
        "price_purchased": 333555,
        "date_listed": "2025-06-19",
        "price_listed": 666444,
        "date_sold": "2025-06-19",
        "price_sold": 1234567,
        "autoteka_link": "https://autoteka.com/autoteka",
        "notes": "123",
        "avito_link": "https://avito.com/avito",
        "autoru_link": "https://auto.ru/autoru",
        "drom_link": "https://drom.com/drom",
        "status": "REPAIRING",
    }


@pytest.mark.asyncio
async def test_cars_create_car_success(client, mock_car_single, get_access_token):
    token = await get_access_token()

    response = await client.post(
        "api/v1/cars/",
        json=mock_car_single,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["result"]["vin"] == mock_car_single["vin"]


@pytest.mark.parametrize("make, expected_status", [("TOTOYA", 404), ("", 422)])
async def test_cars_create_car_invalid_make(
    client, get_access_token, mock_car_single, make, expected_status
):
    token = await get_access_token()
    response = await client.post(
        "api/v1/cars/",
        json={**mock_car_single, "make": make},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == expected_status


@pytest.mark.parametrize("model, expected_status", [("Crola", 404), ("", 422)])
async def test_cars_create_car_invalid_model(
    client, get_access_token, mock_car_single, model, expected_status
):
    token = await get_access_token()
    response = await client.post(
        "api/v1/cars/",
        json={**mock_car_single, "model": model},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == expected_status


@pytest.mark.asyncio
async def test_cars_create_car_unreal_make_model(
    client,
    get_access_token,
    mock_car_single,
):
    token = await get_access_token()
    response = await client.post(
        "api/v1/cars/",
        json={**mock_car_single, "make": "Nissan", "model": "Camry"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404
    assert "Sorry, requested Model does not exist" in response.json()["detail"]


@pytest.mark.parametrize(
    "year, expected_status", [("1950", 422), ("2077", 422), ("", 422)]
)
async def test_cars_create_car_invalid_year(
    client, get_access_token, mock_car_single, year, expected_status
):
    token = await get_access_token()
    response = await client.post(
        "api/v1/cars/",
        json={**mock_car_single, "year": year},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "vin, expected_status",
    [
        ("ЭЮЯ12312312312312", 422),
        ("ACB123", 422),
        ("ACB123ACB123ACB123ACB123", 422),
        ("", 422),
    ],
)
async def test_cars_create_car_invalid_vin(
    client, get_access_token, mock_car_single, vin, expected_status
):
    token = await get_access_token()
    response = await client.post(
        "api/v1/cars/",
        json={**mock_car_single, "vin": vin},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "pts_num, expected_status",
    [
        ("55WY123123123", 422),
        ("55ХВ123123123", 422),
        ("55ХВ123", 422),
        ("", 422),
    ],
)
async def test_cars_create_car_invalid_pts(
    client, get_access_token, mock_car_single, pts_num, expected_status
):
    token = await get_access_token()
    response = await client.post(
        "api/v1/cars/",
        json={**mock_car_single, "pts_num": pts_num},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "sts_num, expected_status",
    [
        ("99AA123123", 422),
        ("9955123123123", 422),
        ("9955123", 422),
        ("", 422),
    ],
)
async def test_cars_create_car_invalid_sts(
    client, get_access_token, mock_car_single, sts_num, expected_status
):
    token = await get_access_token()
    response = await client.post(
        "api/v1/cars/",
        json={**mock_car_single, "sts_num": sts_num},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "date_purchased, expected_status",
    [
        ("2026-06-18", 422),
        ("2024-00-30", 422),
        ("2024-03-55", 422),
        ("20240355", 422),
        ("", 422),
    ],
)
async def test_cars_create_car_invalid_date_purchased(
    client, get_access_token, mock_car_single, date_purchased, expected_status
):
    token = await get_access_token()
    response = await client.post(
        "api/v1/cars/",
        json={**mock_car_single, "date_purchased": date_purchased},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "price_purchased, expected_status",
    [
        ("150", 422),
        ("", 422),
    ],
)
async def test_cars_create_car_invalid_price_purchased(
    client, get_access_token, mock_car_single, price_purchased, expected_status
):
    token = await get_access_token()
    response = await client.post(
        "api/v1/cars/",
        json={**mock_car_single, "price_purchased": price_purchased},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "status, expected_status",
    [
        ("SOMETHING", 422),
        ("", 422),
    ],
)
async def test_cars_create_car_invalid_status(
    client, get_access_token, mock_car_single, status, expected_status
):
    token = await get_access_token()
    response_invalid = await client.post(
        "api/v1/cars/",
        json={**mock_car_single, "status": status},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_invalid.status_code == expected_status


@pytest.mark.asyncio
async def test_cars_create_car_same_vin_conflict(
    client,
    get_access_token,
    mock_car_single,
):
    token = await get_access_token()
    prep_response = await client.post(
        "api/v1/cars/",
        json=mock_car_single,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert prep_response.status_code == 201

    response = await client.post(
        "api/v1/cars/",
        json=mock_car_single,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_cars_create_car_same_vin_sold(
    client,
    get_access_token,
    mock_car_single,
):
    token = await get_access_token()
    prep_response = await client.post(
        "api/v1/cars/",
        json={**mock_car_single, "status": "SOLD"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert prep_response.status_code == 201
    response = await client.post(
        "api/v1/cars/",
        json=mock_car_single,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201


@pytest.mark.parametrize(
    "query, expected_status, expected_length",
    [
        ("", 200, 5),
        ("?page=1&limit=2", 200, 2),
        ("?page=3&limit=2", 200, 1),
        ("?page=2&limit=2", 200, 2),
        ("?page=1&limit=3", 200, 3),
    ],
)
async def test_cars_get_my_cars_paginated(
    client, get_access_token, mock_cars, query, expected_status, expected_length
):
    token = await get_access_token()
    await create_five_mock_cars(client, token, mock_cars)
    response = await client.get(
        f"/api/v1/cars/my_cars{query}", headers={"Authorization": f"Bearer {token}"}
    )
    data = response.json()
    assert response.status_code == expected_status
    assert len(data["result"]["content"]) == expected_length
    get_me = await client.get(
        "/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert get_me.json()["uid"] == data["result"]["content"][0]["primary_owner_uid"]


@pytest.mark.parametrize(
    "sort_by, order, expected_value",
    [
        ("year", "desc", 2017),
        ("year", "asc", 2002),
        ("model", "desc", "Lancer"),
        ("model", "asc", "Accord"),
        ("make", "desc", "Toyota"),
        ("make", "asc", "Honda"),
    ],
)
async def test_cars_get_my_cars_sorted(
    client, get_access_token, mock_cars, sort_by, order, expected_value
):
    token = await get_access_token()
    await create_five_mock_cars(client, token, mock_cars)
    response = await client.get(
        f"/api/v1/cars/my_cars?page=1&limit=10&sort_by={sort_by}&order={order}",
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()
    assert data["result"]["content"][0][sort_by] == expected_value
    get_me = await client.get(
        "/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert get_me.json()["uid"] == data["result"]["content"][0]["primary_owner_uid"]


@pytest.mark.asyncio
async def test_cars_get_car_by_uid_success(client, get_access_token, mock_car_single):
    token = await get_access_token()
    mock_car_single = await create_mock_car(client, token, mock_car_single)

    response = await client.get(
        f"/api/v1/cars/{mock_car_single["uid"]}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()["result"]
    assert data["uid"] == mock_car_single["uid"]


@pytest.mark.asyncio
async def test_cars_get_car_by_uid_no_auth(client, get_access_token, mock_car_single):
    token = await get_access_token()
    mock_car_single = await create_mock_car(client, token, mock_car_single)

    response = await client.get(
        f"/api/v1/cars/{mock_car_single['uid']}",
    )
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]


@pytest.mark.asyncio
async def test_cars_get_car_by_uid_wrong_car_uid(
    client, get_access_token, mock_car_single
):
    token = await get_access_token()
    await create_mock_car(client, token, mock_car_single)

    response = await client.get(
        f"/api/v1/cars/a8df7978-84b6-43eb-87d1-7f9e4ea24b51",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404
    assert "Cars-uid does not exist" in response.json()["detail"]


@pytest.mark.asyncio
async def test_cars_get_car_by_uid_deny_access_to_strangers_car(
    client, mock_car_single, mock_user_factory, override_current_user
):
    user_a = mock_user_factory(role=UserRole.USER)
    override_current_user(user_a)
    response = await client.post("/api/v1/cars/", json=mock_car_single)
    assert response.status_code == 201
    car_uid = response.json()["result"]["uid"]

    user_b = mock_user_factory(role=UserRole.USER)
    override_current_user(user_b)
    response = await client.get(f"/api/v1/cars/{car_uid}")
    assert response.status_code == 403
    assert "Access denied" in response.json()["detail"]


@pytest.mark.asyncio
async def test_cars_get_car_by_uid_admin_access_to_strangers_car(
    client, mock_car_single, mock_user_factory, override_current_user
):
    user = mock_user_factory(role=UserRole.USER)
    override_current_user(user)
    response = await client.post("/api/v1/cars/", json=mock_car_single)
    assert response.status_code == 201
    car_uid = response.json()["result"]["uid"]

    admin = mock_user_factory(role=UserRole.ADMIN)
    override_current_user(admin)
    response = await client.get(f"/api/v1/cars/{car_uid}")
    assert response.status_code == 200
    assert response.json()["result"]["uid"] == car_uid


@pytest.mark.asyncio
async def test_cars_update_car_success(
    client, get_access_token, mock_car_single, mock_car_update
):
    token = await get_access_token()
    car = await create_mock_car(client, token, mock_car_single)

    response = await client.patch(
        f"/api/v1/cars/{car["uid"]}",
        json=mock_car_update,
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["result"]["uid"] == car["uid"]


@pytest.mark.parametrize(
    "invalid_fields",
    [
        {
            "status": "something",
        },
        {
            "price_purchased": 1,
        },
        {
            "date_listed": "2077-06-19",
        },
        {
            "price_listed": "321asd",
        },
        {
            "date_sold": "2077-06-19",
        },
        {
            "price_sold": 3,
        },
        {
            "autoteka_link": 1234,
        },
        {
            "notes": 123465,
        },
        {
            "avito_link": 1236572,
        },
        {
            "autoru_link": 135785,
        },
    ],
)
async def test_cars_update_car_invalid_data(
    client, get_access_token, mock_car_single, mock_car_update, invalid_fields
):
    token = await get_access_token()
    car = await create_mock_car(client, token, mock_car_single)
    car_uid = car["uid"]

    response = await client.patch(
        f"/api/v1/cars/{car_uid}",
        json={**mock_car_update, **invalid_fields},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422


@pytest.mark.parametrize(
    "role, expected_status",
    [
        (UserRole.ADMIN, 200),
        (UserRole.USER, 403),
    ],
)
async def test_cars_update_car_stranger_car(
    client,
    mock_car_single,
    mock_user_factory,
    override_current_user,
    mock_car_update,
    role,
    expected_status,
):
    user_a = mock_user_factory(role=UserRole.USER)
    override_current_user(user_a)
    response = await client.post("/api/v1/cars/", json=mock_car_single)
    assert response.status_code == 201
    car_uid = response.json()["result"]["uid"]

    user_b = mock_user_factory(role=role)
    override_current_user(user_b)
    response = await client.patch(f"/api/v1/cars/{car_uid}", json=mock_car_update)
    assert response.status_code == expected_status


@pytest.mark.asyncio
async def test_cars_delete_car_success(client, get_access_token, mock_car_single):
    token = await get_access_token()
    car = await create_mock_car(client, token, mock_car_single)
    response = await client.delete(
        f"/api/v1/cars/{car['uid']}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_cars_delete_car_unauthorized(client, mock_car_single, get_access_token):
    token = await get_access_token()
    car = await create_mock_car(client, token, mock_car_single)
    response = await client.delete(f"/api/v1/cars/{car['uid']}")

    assert response.status_code == 401


@pytest.mark.parametrize(
    "role, expected_status",
    [
        (UserRole.ADMIN, 204),
        (UserRole.USER, 403),
    ],
)
async def test_cars_delete_car_stranger_car(
    client,
    mock_car_single,
    mock_user_factory,
    override_current_user,
    role,
    expected_status,
):
    user_a = mock_user_factory(role=UserRole.USER)
    override_current_user(user_a)
    response = await client.post("/api/v1/cars/", json=mock_car_single)
    assert response.status_code == 201
    car_uid = response.json()["result"]["uid"]

    user_b = mock_user_factory(role=role)
    override_current_user(user_b)
    response = await client.delete(f"/api/v1/cars/{car_uid}")
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "role, expected_status",
    [
        (UserRole.ADMIN, 200),
        (UserRole.USER, 403),
    ],
)
async def test_cars_get_all_cars_filtered_access(
    client,
    mock_user_factory,
    role,
    expected_status,
    get_access_token,
    mock_cars,
    override_current_user,
):
    user_a = mock_user_factory(role=UserRole.USER)
    override_current_user(user_a)
    for car in mock_cars:
        response = await client.post("/api/v1/cars/", json=car)
        assert response.status_code == 201

    user_b = mock_user_factory(role=role)
    override_current_user(user_b)
    response = await client.post(
        "/api/v1/cars/all",
        json={
            "page": 1,
            "limit": 10,
            "status": "FRESH",
            "sort_by": "created_at",
            "order_desc": "desc",
        },
    )
    assert response.status_code == expected_status
    if role == UserRole.ADMIN:
        assert len(response.json()["result"]["content"]) == 5
        response = await client.post(
            "/api/v1/cars/all",
            json={"page": 2, "limit": 3, "sort_by": "year", "order_desc": "asc"},
        )
        assert response.status_code == 200
        assert len(response.json()["result"]["content"]) == 2
        assert response.json()["result"]["content"][1]["year"] == 2017
