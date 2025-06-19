import pytest


mock_car_list = [
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

mock_car = mock_car_list[0]


@pytest.mark.asyncio
async def test_cars_create_car_success(client, get_access_token):
    token = await get_access_token()

    response = await client.post(
        "api/v1/cars/",
        json=mock_car,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["result"]["vin"] == mock_car["vin"]


@pytest.mark.parametrize("make, expected_status", [("TOTOYA", 404), ("", 422)])
async def test_cars_create_car_invalid_make(
    client, get_access_token, make, expected_status
):
    token = await get_access_token()
    response = await client.post(
        "api/v1/cars/",
        json={**mock_car, "make": make},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == expected_status


@pytest.mark.parametrize("model, expected_status", [("Crola", 404), ("", 422)])
async def test_cars_create_car_invalid_model(
    client, get_access_token, model, expected_status
):
    token = await get_access_token()
    response = await client.post(
        "api/v1/cars/",
        json={**mock_car, "model": model},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == expected_status


@pytest.mark.asyncio
async def test_cars_create_car_unreal_make_model(client, get_access_token):
    token = await get_access_token()
    response = await client.post(
        "api/v1/cars/",
        json={**mock_car, "make": "Nissan", "model": "Camry"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404
    assert "Sorry, requested Model does not exist" in response.json()["detail"]


@pytest.mark.parametrize(
    "year, expected_status", [("1950", 422), ("2077", 422), ("", 422)]
)
async def test_cars_create_car_invalid_year(
    client, get_access_token, year, expected_status
):
    token = await get_access_token()
    response = await client.post(
        "api/v1/cars/",
        json={**mock_car, "year": year},
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
    client, get_access_token, vin, expected_status
):
    token = await get_access_token()
    response = await client.post(
        "api/v1/cars/",
        json={**mock_car, "vin": vin},
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
    client, get_access_token, pts_num, expected_status
):
    token = await get_access_token()
    response = await client.post(
        "api/v1/cars/",
        json={**mock_car, "pts_num": pts_num},
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
    client, get_access_token, sts_num, expected_status
):
    token = await get_access_token()
    response = await client.post(
        "api/v1/cars/",
        json={**mock_car, "sts_num": sts_num},
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
    client, get_access_token, date_purchased, expected_status
):
    token = await get_access_token()
    response = await client.post(
        "api/v1/cars/",
        json={**mock_car, "date_purchased": date_purchased},
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
    client, get_access_token, price_purchased, expected_status
):
    token = await get_access_token()
    response = await client.post(
        "api/v1/cars/",
        json={**mock_car, "price_purchased": price_purchased},
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
    client, get_access_token, status, expected_status
):
    token = await get_access_token()
    response_invalid = await client.post(
        "api/v1/cars/",
        json={**mock_car, "status": status},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_invalid.status_code == expected_status


@pytest.mark.asyncio
async def test_cars_create_car_same_vin_conflict(client, get_access_token):
    token = await get_access_token()
    prep_response = await client.post(
        "api/v1/cars/",
        json=mock_car,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert prep_response.status_code == 201

    response = await client.post(
        "api/v1/cars/",
        json=mock_car,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_cars_create_car_same_vin_sold(client, get_access_token):
    token = await get_access_token()
    prep_response = await client.post(
        "api/v1/cars/",
        json={**mock_car, "status": "SOLD"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert prep_response.status_code == 201
    response = await client.post(
        "api/v1/cars/",
        json=mock_car,
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
        ("?page=10&limit=10", 200, 0),
    ],
)
async def test_cars_get_my_cars_paginated(
    client, get_access_token, query, expected_status, expected_length
):
    token = await get_access_token()
    for car in mock_car_list:
        response = await client.post(
            "/api/v1/cars/",
            json=car,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
    response = await client.get(
        f"/api/v1/cars/my_cars{query}", headers={"Authorization": f"Bearer {token}"}
    )
    data = response.json()
    assert response.status_code == expected_status
    assert len(data["result"]["content"]) == expected_length


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
    client, get_access_token, sort_by, order, expected_value
):
    token = await get_access_token()
    for car in mock_car_list:
        response = await client.post(
            "/api/v1/cars/",
            json=car,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
    response = await client.get(
        f"/api/v1/cars/my_cars?page=1&limit=10&sort_by={sort_by}&order={order}",
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()
    assert data["result"]["content"][0][sort_by] == expected_value
