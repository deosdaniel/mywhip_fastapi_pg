from uuid import UUID, uuid4

import pytest

from src.users.schemas import UserRole
from tests.cars.cars_helpers import (
    create_mock_car,
    create_mock_expense,
    create_mock_car_w_exp,
)
from tests.cars.test_cars import mock_car_single


@pytest.fixture
def mock_expense_single():
    return {"name": "Some Expense", "exp_summ": 5000}


@pytest.fixture
def mock_expenses():
    return [
        {"name": "Expense #1", "exp_summ": 5000},
        {"name": "Expense #2", "exp_summ": 4000},
        {"name": "Expense #3", "exp_summ": 3000},
        {"name": "Expense #4", "exp_summ": 2000},
        {"name": "Expense #5", "exp_summ": 1000},
    ]


@pytest.mark.asyncio
async def test_expenses_create_expense_success(
    client, get_access_token, mock_car_single, mock_expense_single
):
    token = await get_access_token()
    mock_car = await create_mock_car(client, token, mock_car_single)
    car_uid = mock_car["uid"]
    response = await client.post(
        f"api/v1/cars/{car_uid}",
        json=mock_expense_single,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_expenses_create_expense_no_auth(
    client, get_access_token, mock_car_single, mock_expense_single
):
    token = await get_access_token()
    mock_car = await create_mock_car(client, token, mock_car_single)
    car_uid = mock_car["uid"]
    response = await client.post(f"api/v1/cars/{car_uid}", json=mock_expense_single)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_expenses_create_expense_strangers_car(
    client,
    mock_car_single,
    mock_user_factory,
    override_current_user,
    mock_expense_single,
):
    user_a = mock_user_factory(role=UserRole.USER)
    override_current_user(user_a)
    response = await client.post("/api/v1/cars/", json=mock_car_single)
    assert response.status_code == 201
    car_uid = response.json()["result"]["uid"]

    user_b = mock_user_factory(role=UserRole.USER)
    override_current_user(user_b)
    response = await client.post(f"api/v1/cars/{car_uid}", json=mock_expense_single)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_expenses_create_expense_nonexistent_car(
    client,
    mock_car_single,
    mock_user_factory,
    override_current_user,
    mock_expense_single,
):
    user_a = mock_user_factory(role=UserRole.USER)
    override_current_user(user_a)
    response = await client.post(f"api/v1/cars/{uuid4()}", json=mock_expense_single)
    assert response.status_code == 404


@pytest.mark.parametrize(
    "exp_name, summ, expected_status",
    [
        ("", 5000, 422),
        (1337, 5000, 422),
        ("ExpenseName", 0, 422),
        ("ExpenseName", -1000, 422),
        ("ExpenseName", "randomstring", 422),
        ("", "", 422),
    ],
)
async def test_expenses_create_expense_invalid_data(
    client, get_access_token, mock_car_single, exp_name, summ, expected_status
):
    token = await get_access_token()
    mock_car = await create_mock_car(client, token, mock_car_single)
    car_uid = mock_car["uid"]
    response = await client.post(
        f"api/v1/cars/{car_uid}",
        json={"name": exp_name, "exp_summ": summ},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == expected_status


@pytest.mark.asyncio
async def test_expenses_get_single_exp_success(
    client, get_access_token, mock_car_single
):
    token = await get_access_token()

    mock_car = await create_mock_car(client, token, mock_car_single)
    car_uid = mock_car["uid"]

    mock_exp = await create_mock_expense(client, car_uid, token)
    exp_uid = mock_exp["uid"]

    response = await client.get(
        f"/api/v1/cars/{car_uid}/expenses/{exp_uid}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_expenses_get_single_exp_invalid_car(
    client, get_access_token, mock_car_single
):
    token = await get_access_token()

    mock_car = await create_mock_car(client, token, mock_car_single)
    car_uid = mock_car["uid"]

    mock_exp = await create_mock_expense(client, car_uid, token)
    exp_uid = mock_exp["uid"]

    response = await client.get(
        f"/api/v1/cars/{uuid4()}/expenses/{exp_uid}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_expenses_get_single_exp_invalid_exp(
    client, get_access_token, mock_car_single
):
    token = await get_access_token()

    mock_car = await create_mock_car(client, token, mock_car_single)
    car_uid = mock_car["uid"]

    await create_mock_expense(client, car_uid, token)

    response = await client.get(
        f"/api/v1/cars/{car_uid}/expenses/{uuid4()}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


@pytest.mark.parametrize(
    "role, expected_status", [(UserRole.ADMIN, 200), (UserRole.USER, 403)]
)
async def test_expenses_get_single_exp_strangers_car(
    client,
    mock_car_single,
    mock_user_factory,
    override_current_user,
    role,
    expected_status,
    mock_expense_single,
):
    user_a = mock_user_factory(role=UserRole.USER)
    override_current_user(user_a)
    response = await client.post("/api/v1/cars/", json=mock_car_single)
    assert response.status_code == 201
    car_uid = response.json()["result"]["uid"]
    response = await client.post(f"/api/v1/cars/{car_uid}", json=mock_expense_single)
    assert response.status_code == 201
    exp_uid = response.json()["result"]["uid"]

    user_b = mock_user_factory(role=role)
    override_current_user(user_b)
    response = await client.get(f"/api/v1/cars/{car_uid}/expenses/{exp_uid}")
    assert response.status_code == expected_status
    if role == UserRole.USER:
        assert "Access denied" in response.json()["detail"]


@pytest.mark.asyncio
async def test_expenses_update_single_exp_success(
    client, get_access_token, mock_car_single
):
    token = await get_access_token()

    car = await create_mock_car_w_exp(client, token, mock_car_single)
    car_uid = car["car_uid"]
    exp_uid = car["exp_uid"]

    response = await client.patch(
        f"/api/v1/cars/{car_uid}/expenses/{exp_uid}",
        json={"name": "Updated Expense", "exp_summ": 2050},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()["result"]
    assert data["name"] == "Updated Expense"
    assert data["exp_summ"] == 2050


@pytest.mark.parametrize(
    "exp_name, summ, expected_status",
    [
        ("", 5000, 422),
        (1337, 5000, 422),
        ("ExpenseName", 0, 422),
        ("ExpenseName", -1000, 422),
        ("ExpenseName", "randomstring", 422),
        ("", "", 422),
    ],
)
async def test_expenses_update_expense_invalid_data(
    client, get_access_token, mock_car_single, exp_name, summ, expected_status
):
    token = await get_access_token()
    car = await create_mock_car_w_exp(client, token, mock_car_single)
    car_uid = car["car_uid"]
    exp_uid = car["exp_uid"]

    response = await client.patch(
        f"api/v1/cars/{car_uid}/expenses/{exp_uid}",
        json={"name": exp_name, "exp_summ": summ},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == expected_status


@pytest.mark.asyncio
async def test_expenses_update_single_exp_no_auth(
    client, get_access_token, mock_car_single
):
    token = await get_access_token()

    car = await create_mock_car_w_exp(client, token, mock_car_single)
    car_uid = car["car_uid"]
    exp_uid = car["exp_uid"]

    response = await client.patch(
        f"/api/v1/cars/{car_uid}/expenses/{exp_uid}",
        json={"name": "Updated Expense", "exp_summ": 2050},
    )
    assert response.status_code == 401


@pytest.mark.parametrize(
    "role, expected_status", [(UserRole.ADMIN, 200), (UserRole.USER, 403)]
)
async def test_expenses_update_single_exp_strangers_car(
    client,
    mock_car_single,
    mock_user_factory,
    override_current_user,
    role,
    expected_status,
    mock_expense_single,
):
    user_a = mock_user_factory(role=UserRole.USER)
    override_current_user(user_a)
    response = await client.post("/api/v1/cars/", json=mock_car_single)
    assert response.status_code == 201
    car_uid = response.json()["result"]["uid"]
    response = await client.post(f"/api/v1/cars/{car_uid}", json=mock_expense_single)
    assert response.status_code == 201
    exp_uid = response.json()["result"]["uid"]

    user_b = mock_user_factory(role=role)
    override_current_user(user_b)
    response = await client.patch(
        f"/api/v1/cars/{car_uid}/expenses/{exp_uid}",
        json={"name": "Updated Expense", "exp_summ": 2050},
    )
    assert response.status_code == expected_status
    if role == UserRole.USER:
        assert "Access denied" in response.json()["detail"]
    if role == UserRole.ADMIN:
        assert response.json()["result"]["name"] == "Updated Expense"


@pytest.mark.asyncio
async def test_expenses_delete_single_exp(client, get_access_token, mock_car_single):
    token = await get_access_token()
    car = await create_mock_car_w_exp(client, token, mock_car_single)
    car_uid = car["car_uid"]
    exp_uid = car["exp_uid"]
    response = await client.delete(
        f"/api/v1/cars/{car_uid}/expenses/{exp_uid}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 204
    response = await client.delete(
        f"/api/v1/cars/{car_uid}/expenses/{exp_uid}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


@pytest.mark.parametrize(
    "role, expected_status", [(UserRole.ADMIN, 204), (UserRole.USER, 403)]
)
async def test_expenses_update_single_exp_strangers_car(
    client,
    mock_car_single,
    mock_user_factory,
    override_current_user,
    role,
    expected_status,
    mock_expense_single,
):
    user_a = mock_user_factory(role=UserRole.USER)
    override_current_user(user_a)
    response = await client.post("/api/v1/cars/", json=mock_car_single)
    assert response.status_code == 201
    car_uid = response.json()["result"]["uid"]
    response = await client.post(f"/api/v1/cars/{car_uid}", json=mock_expense_single)
    assert response.status_code == 201
    exp_uid = response.json()["result"]["uid"]

    user_b = mock_user_factory(role=role)
    override_current_user(user_b)
    response = await client.delete(f"/api/v1/cars/{car_uid}/expenses/{exp_uid}")
    assert response.status_code == expected_status


@pytest.mark.asyncio
async def test_expenses_get_all_exp(
    client, mock_car_single, mock_user_factory, override_current_user, mock_expenses
):
    user_a = mock_user_factory(role=UserRole.USER)
    override_current_user(user_a)
    response = await client.post("/api/v1/cars/", json=mock_car_single)
    assert response.status_code == 201
    car_uid = response.json()["result"]["uid"]
    for exp in mock_expenses:
        response = await client.post(f"/api/v1/cars/{car_uid}", json=exp)
        assert response.status_code == 201

    response = await client.get(f"/api/v1/cars/{car_uid}/expenses")
    assert response.status_code == 200
    assert len(response.json()["result"]["content"]) == 5
    response = await client.get(f"/api/v1/cars/{uuid4()}/expenses")
    assert response.status_code == 404
    response = await client.get(
        f"/api/v1/cars/{car_uid}/expenses?page=2&limit=2&sort_by=created_at&order=desc"
    )
    assert response.status_code == 200
    assert len(response.json()["result"]["content"]) == 2
    response = await client.get(
        f"/api/v1/cars/{car_uid}/expenses?page=3&limit=2&sort_by=created_at&order=desc"
    )
    assert response.status_code == 200
    assert len(response.json()["result"]["content"]) == 1
    response = await client.get(
        f"/api/v1/cars/{car_uid}/expenses?sort_by=exp_summ&order=asc"
    )
    assert response.status_code == 200
    assert response.json()["result"]["content"][0]["exp_summ"] == 1000
    response = await client.get(
        f"/api/v1/cars/{car_uid}/expenses?sort_by=exp_summ&order=invalid"
    )
    assert response.status_code == 422
    response = await client.get(
        f"/api/v1/cars/{car_uid}/expenses?sort_by=invalid&order=asc"
    )
    assert response.status_code == 400


@pytest.mark.parametrize(
    "role, expected_status",
    [
        (UserRole.ADMIN, 200),
        (UserRole.USER, 403),
    ],
)
async def test_expenses_get_all_exp_strangers_car(
    client,
    mock_car_single,
    mock_user_factory,
    override_current_user,
    mock_expenses,
    role,
    expected_status,
):
    user_a = mock_user_factory(role=UserRole.USER)
    override_current_user(user_a)
    response = await client.post("/api/v1/cars/", json=mock_car_single)
    assert response.status_code == 201
    car_uid = response.json()["result"]["uid"]
    for exp in mock_expenses:
        response = await client.post(f"/api/v1/cars/{car_uid}", json=exp)
        assert response.status_code == 201

    response = await client.get(f"/api/v1/cars/{car_uid}/expenses")
    assert response.status_code == 200

    user_b = mock_user_factory(role=role)
    override_current_user(user_b)
    response = await client.get(f"/api/v1/cars/{car_uid}/expenses")
    assert response.status_code == expected_status


@pytest.mark.asyncio
async def test_expenses_delete_all_exp(
    client, mock_car_single, mock_user_factory, override_current_user, mock_expenses
):
    user_a = mock_user_factory(role=UserRole.USER)
    override_current_user(user_a)
    response = await client.post("/api/v1/cars/", json=mock_car_single)
    assert response.status_code == 201
    car_uid = response.json()["result"]["uid"]

    for exp in mock_expenses:
        response = await client.post(f"/api/v1/cars/{car_uid}", json=exp)
        assert response.status_code == 201
    response = await client.delete(f"/api/v1/cars/{uuid4()}/expenses")
    assert response.status_code == 404
    response = await client.delete(f"/api/v1/cars/{car_uid}/expenses")
    assert response.status_code == 204
    response = await client.delete(f"/api/v1/cars/{car_uid}/expenses")
    assert response.status_code == 204


@pytest.mark.parametrize(
    "role, expected_status",
    [
        (UserRole.ADMIN, 204),
        (UserRole.USER, 403),
    ],
)
async def test_expenses_delete_all_exp_strangers_car(
    client,
    mock_car_single,
    mock_user_factory,
    override_current_user,
    mock_expenses,
    role,
    expected_status,
):
    user_a = mock_user_factory(role=UserRole.USER)
    override_current_user(user_a)
    response = await client.post("/api/v1/cars/", json=mock_car_single)
    assert response.status_code == 201
    car_uid = response.json()["result"]["uid"]
    for exp in mock_expenses:
        response = await client.post(f"/api/v1/cars/{car_uid}", json=exp)
        assert response.status_code == 201

    user_b = mock_user_factory(role=role)
    override_current_user(user_b)
    response = await client.delete(f"/api/v1/cars/{car_uid}/expenses")
    assert response.status_code == expected_status
