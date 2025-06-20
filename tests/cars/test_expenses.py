from uuid import UUID, uuid4

import pytest

from src.users.schemas import UserRole
from tests.cars.cars_helpers import create_mock_car, create_mock_expense
from tests.cars.test_cars import mock_car

exp_dict = {"name": "Some Expense", "exp_summ": 5000}


@pytest.mark.asyncio
async def test_expenses_create_expense_success(client, get_access_token, mock_car):
    token = await get_access_token()
    mock_car = await create_mock_car(client, token, mock_car)
    car_uid = mock_car["uid"]
    response = await client.post(
        f"api/v1/cars/{car_uid}",
        json=exp_dict,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_expenses_create_expense_no_auth(client, get_access_token, mock_car):
    token = await get_access_token()
    mock_car = await create_mock_car(client, token, mock_car)
    car_uid = mock_car["uid"]
    response = await client.post(f"api/v1/cars/{car_uid}", json=exp_dict)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_expenses_create_expense_strangers_car(
    client, mock_car, mock_user_factory, override_current_user
):
    user_a = mock_user_factory(role=UserRole.USER)
    override_current_user(user_a)
    response = await client.post("/api/v1/cars/", json=mock_car)
    assert response.status_code == 201
    car_uid = response.json()["result"]["uid"]

    user_b = mock_user_factory(role=UserRole.USER)
    override_current_user(user_b)
    response = await client.post(f"api/v1/cars/{car_uid}", json=exp_dict)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_expenses_create_expense_nonexistent_car(
    client, mock_car, mock_user_factory, override_current_user
):
    user_a = mock_user_factory(role=UserRole.USER)
    override_current_user(user_a)
    response = await client.post(f"api/v1/cars/{uuid4()}", json=exp_dict)
    assert response.status_code == 404


@pytest.mark.parametrize(
    "exp_name, summ, expected_status",
    [
        ("", 5000, 422),
        (1337, 5000, 422),
        ("ExpenseName", 0, 422),
        ("ExpenseName", -1000, 422),
        ("ExpenseName", "randomstring", 422),
    ],
)
async def test_expenses_create_expense_invalid_data(
    client, get_access_token, mock_car, exp_name, summ, expected_status
):
    token = await get_access_token()
    mock_car = await create_mock_car(client, token, mock_car)
    car_uid = mock_car["uid"]
    response = await client.post(
        f"api/v1/cars/{car_uid}",
        json={"name": exp_name, "exp_summ": summ},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == expected_status


@pytest.mark.asyncio
async def test_expenses_get_by_uid(client, get_access_token, mock_car):
    token = await get_access_token()

    mock_car = await create_mock_car(client, token, mock_car)
    car_uid = mock_car["uid"]

    mock_exp = await create_mock_expense(client, car_uid, token)
    exp_uid = mock_exp["uid"]

    response = await client.get(
        f"/api/v1/cars/{car_uid}/expenses/{exp_uid}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
