async def create_mock_car(client, token: str, car_data: dict) -> dict:
    response = await client.post(
        "/api/v1/cars/",
        json=car_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    return response.json()["result"]
