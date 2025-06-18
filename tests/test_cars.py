from http.client import responses

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
        "price_purchased": 100500,
        "status": "FRESH",
    },
    {
        "make": "Honda",
        "model": "Accord",
        "year": 2002,
        "vin": "JZX10012345678902",
        "pts_num": "55ХВ123123",
        "sts_num": "9955123123",
        "date_purchased": "2025-06-18",
        "price_purchased": 100500,
        "status": "FRESH",
    },
    {
        "make": "Mitsubishi",
        "model": "Lancer",
        "year": 2007,
        "vin": "JZX10012345678903",
        "pts_num": "55ХВ123123",
        "sts_num": "9955123123",
        "date_purchased": "2025-06-18",
        "price_purchased": 100500,
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


@pytest.mark.asyncio
async def test_cars_create_car_invalid_make(client, get_access_token):
    token = await get_access_token()
    response = await client.post(
        "api/v1/cars/",
        json={**car_data, "make": "TOTOYA"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404
    assert "Sorry, requested Make does not exist" in response.json()["detail"]

    response_empty = await client.post(
        "api/v1/cars/",
        json={**car_data, "make": ""},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_empty.status_code == 422


@pytest.mark.asyncio
async def test_cars_create_car_invalid_model(client, get_access_token):
    token = await get_access_token()
    response = await client.post(
        "api/v1/cars/",
        json={**car_data, "model": "Crola"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404
    assert "Sorry, requested Model does not exist" in response.json()["detail"]

    response_empty = await client.post(
        "api/v1/cars/",
        json={**car_data, "model": ""},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_empty.status_code == 422


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


@pytest.mark.asyncio
async def test_cars_create_car_invalid_year(client, get_access_token):
    token = await get_access_token()
    response_past = await client.post(
        "api/v1/cars/",
        json={**car_data, "year": "1950"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_past.status_code == 422

    response_future = await client.post(
        "api/v1/cars/",
        json={**car_data, "year": "2035"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_future.status_code == 422

    response_empty = await client.post(
        "api/v1/cars/",
        json={**car_data, "year": ""},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_empty.status_code == 422


@pytest.mark.asyncio
async def test_cars_create_car_invalid_vin(client, get_access_token):
    token = await get_access_token()
    response_cyrillic = await client.post(
        "api/v1/cars/",
        json={**car_data, "vin": "ЭЮЯ12312312312312"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_cyrillic.status_code == 422

    response_short = await client.post(
        "api/v1/cars/",
        json={**car_data, "vin": "ACB123"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_short.status_code == 422

    response_long = await client.post(
        "api/v1/cars/",
        json={**car_data, "vin": "ACB123ACB123ACB123ACB123"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_long.status_code == 422

    response_empty = await client.post(
        "api/v1/cars/",
        json={**car_data, "vin": ""},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_empty.status_code == 422


@pytest.mark.asyncio
async def test_cars_create_car_invalid_pts(client, get_access_token):
    token = await get_access_token()
    response_latin = await client.post(
        "api/v1/cars/",
        json={**car_data, "pts_num": "55WW123123"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_latin.status_code == 422

    response_long = await client.post(
        "api/v1/cars/",
        json={**car_data, "pts_num": "55ХВ123123123"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_long.status_code == 422

    response_short = await client.post(
        "api/v1/cars/",
        json={**car_data, "pts_num": "55ХВ123"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_short.status_code == 422

    response_empty = await client.post(
        "api/v1/cars/",
        json={**car_data, "pts_num": ""},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_empty.status_code == 422


@pytest.mark.asyncio
async def test_cars_create_car_invalid_sts(client, get_access_token):
    token = await get_access_token()
    response_letters = await client.post(
        "api/v1/cars/",
        json={**car_data, "sts_num": "99УЮ123123"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_letters.status_code == 422

    response_long = await client.post(
        "api/v1/cars/",
        json={**car_data, "sts_num": "9955123123123"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_long.status_code == 422

    response_short = await client.post(
        "api/v1/cars/",
        json={**car_data, "sts_num": "9955123"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_short.status_code == 422

    response_empty = await client.post(
        "api/v1/cars/",
        json={**car_data, "sts_num": ""},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_empty.status_code == 422


@pytest.mark.asyncio
async def test_cars_create_car_invalid_date_purchased(client, get_access_token):
    token = await get_access_token()
    response_future = await client.post(
        "api/v1/cars/",
        json={**car_data, "date_purchased": "2026-06-18"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_future.status_code == 422

    response_invalid_month = await client.post(
        "api/v1/cars/",
        json={**car_data, "date_purchased": "2024-00-30"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_invalid_month.status_code == 422

    response_invalid_day = await client.post(
        "api/v1/cars/",
        json={**car_data, "date_purchased": "2024-03-55"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_invalid_day.status_code == 422

    response_invalid_format = await client.post(
        "api/v1/cars/",
        json={**car_data, "date_purchased": "20240355"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_invalid_format.status_code == 422

    response_empty = await client.post(
        "api/v1/cars/",
        json={**car_data, "date_purchased": ""},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_empty.status_code == 422


@pytest.mark.asyncio
async def test_cars_create_car_invalid_price_purchased(client, get_access_token):
    token = await get_access_token()
    response_too_cheap = await client.post(
        "api/v1/cars/",
        json={**car_data, "price_purchased": "150"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_too_cheap.status_code == 422
    response_empty = await client.post(
        "api/v1/cars/",
        json={**car_data, "price_purchased": ""},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_empty.status_code == 422


@pytest.mark.asyncio
async def test_cars_create_car_invalid_status(client, get_access_token):
    token = await get_access_token()
    response_invalid = await client.post(
        "api/v1/cars/",
        json={**car_data, "status": "SOMETHING"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_invalid.status_code == 422
    response_empty = await client.post(
        "api/v1/cars/",
        json={**car_data, "status": ""},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_empty.status_code == 422


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
    assert len(data["result"]["content"]) == 3
