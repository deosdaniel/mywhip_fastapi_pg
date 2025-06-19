import pytest


car_data = {
    "make": "Toyota",
    "model": "Corolla",
    "year": 2005,
    "vin": "JZX10012345678901",
    "pts_num": "55ХВ123123",
    "sts_num": "9955123123",
    "date_purchased": "2025-06-18",
    "price_purchased": 100500,
    "status": "FRESH",
}

car_list = [
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


@pytest.mark.asyncio
async def test_cars_create_car_success(client, get_access_token):
    token = await get_access_token()

    response = await client.post(
        "api/v1/cars/", json=car_data, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["result"]["vin"] == car_data["vin"]


@pytest.mark.parametrize("make, expected_status", [("TOTOYA", 404), ("", 422)])
async def test_cars_create_car_invalid_make(
    client, get_access_token, make, expected_status
):
    token = await get_access_token()
    response = await client.post(
        "api/v1/cars/",
        json={**car_data, "make": make},
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
        json={**car_data, "model": model},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == expected_status


@pytest.mark.asyncio
async def test_cars_create_car_unreal_make_model(client, get_access_token):
    token = await get_access_token()
    response = await client.post(
        "api/v1/cars/",
        json={**car_data, "make": "Nissan", "model": "Camry"},
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
        json={**car_data, "year": year},
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
        json={**car_data, "vin": vin},
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
        json={**car_data, "pts_num": pts_num},
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
        json={**car_data, "sts_num": sts_num},
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
        json={**car_data, "date_purchased": date_purchased},
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
        json={**car_data, "price_purchased": price_purchased},
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
        json={**car_data, "status": status},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_invalid.status_code == expected_status


@pytest.mark.asyncio
async def test_cars_create_car_same_vin_conflict(client, get_access_token):
    token = await get_access_token()
    prep_response = await client.post(
        "api/v1/cars/", json=car_data, headers={"Authorization": f"Bearer {token}"}
    )
    assert prep_response.status_code == 201

    response = await client.post(
        "api/v1/cars/", json=car_data, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_cars_create_car_same_vin_sold(client, get_access_token):
    token = await get_access_token()
    prep_response = await client.post(
        "api/v1/cars/",
        json={**car_data, "status": "SOLD"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert prep_response.status_code == 201
    response = await client.post(
        "api/v1/cars/",
        json=car_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_cars_get_my_cars_success(client, get_access_token):
    token = await get_access_token()
    for car in car_list:
        response = await client.post(
            "/api/v1/cars/",
            json=car,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
    response = await client.get(
        "/api/v1/cars/my_cars", headers={"Authorization": f"Bearer {token}"}
    )
    data = response.json()
    assert response.status_code == 200
    assert len(data["result"]["content"]) == 5

    response = await client.get(
        "/api/v1/cars/my_cars?page=1&limit=2",
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()
    assert len(data["result"]["content"]) == 2

    response = await client.get(
        "/api/v1/cars/my_cars?page=3&limit=2",
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()
    assert len(data["result"]["content"]) == 1

    response = await client.get(
        "/api/v1/cars/my_cars?page=2&limit=2&sort_by=year&order=desc",
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()
    assert data["result"]["content"][0]["year"] > data["result"]["content"][1]["year"]
    assert len(data["result"]["content"]) == 2

    response = await client.get(
        "/api/v1/cars/my_cars?page=1&limit=3&sort_by=year&order=asc",
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()
    assert data["result"]["content"][0]["year"] < data["result"]["content"][1]["year"]
    assert len(data["result"]["content"]) == 3
