import uuid

import pytest
from tests.cars.cars_helpers import create_mock_car
from tests.cars.test_cars import mock_car

exp_dict = {
  "name": "string",
  "exp_summ": 1
}

@pytest.mark.asyncio
async def test_expenses_create_expense_success(client, get_access_token, mock_car):
    token = await get_access_token()
    mock_car = await create_mock_car(client, token, mock_car)
    response = await client.post(f"api/v1/cars/{mock_car["uid"]}", json=exp_dict, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201