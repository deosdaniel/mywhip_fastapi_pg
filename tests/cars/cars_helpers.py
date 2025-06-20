async def create_mock_car(client, token: str, car_data: dict) -> dict:
    response = await client.post(
        "/api/v1/cars/",
        json=car_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    return response.json()["result"]


async def create_mock_expense(client, car_uid: str, token: str):
    response = await client.post(
        f"/api/v1/cars/{car_uid}",
        json={"name": "Mock Expense", "exp_summ": 5000},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    return response.json()["result"]


async def create_mock_car_w_exp(client, token: str, car_data: dict) -> dict:
    response = await client.post(
        "/api/v1/cars/",
        json=car_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    car_uid = response.json()["result"]["uid"]
    response = await client.post(
        f"/api/v1/cars/{car_uid}",
        json={"name": "Mock Expense", "exp_summ": 5000},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    response = await client.get(f"/api/v1/cars/{car_uid}")
    assert response.status_code == 200
    return response.json()["result"]


async def create_five_mock_cars(client, token: str, cars_data: dict) -> dict:
    created_cars = []
    for car in cars_data:
        response = await client.post(
            "/api/v1/cars/",
            json=car,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
        created_cars.append(response.json()["result"])
    return created_cars
