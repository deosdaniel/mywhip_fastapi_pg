from datetime import datetime

import pytest

from src.cars.schemas import CarStatusChoices

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


@pytest.mark.asyncio
async def test_cars(client, get_access_token):
    token = await get_access_token()

    response = await client.post(
        "api/v1/cars/", json=car_data, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
