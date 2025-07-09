from fastapi import APIRouter, status, Path, Depends, Query
from sqlmodel import SQLModel

from src.auth.dependencies import get_current_user, require_admin, require_self_or_admin
from src.cars.dependencies import get_exp_service, get_car_service
from src.cars.models import Cars
from src.cars.service import CarService, ExpensesService
from src.users.schemas import UserSchema
from src.utils.schemas_common import ResponseSchema, PageResponse
from src.cars.schemas import (
    CarUpdateSchema,
    CarCreateSchema,
    ExpensesSchema,
    ExpensesCreateSchema,
    CarSchema,
    GetAllFilter,
    CarCreateResponse,
    CarOwners,
)

car_router = APIRouter()
expenses_router = APIRouter()


# Create a Car
@car_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseSchema[CarCreateResponse],
)
async def create_car(
    car_data: CarCreateSchema,
    car_service: CarService = Depends(get_car_service),
    current_user: UserSchema = Depends(get_current_user),
) -> dict:
    result = await car_service.create_car(
        car_data=car_data, primary_owner_uid=current_user.uid
    )
    return ResponseSchema(detail="Success", result=result)


@car_router.get(
    "/my_cars",
    response_model=ResponseSchema[PageResponse[CarSchema]],
    response_model_exclude_none=True,
)
async def get_my_cars(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1),
    sort_by: str = Query(default="created_at", description="Поле сортировки"),
    order: str = Query(
        default="desc", pattern="^(asc|desc)$", description="Порядок сортировки"
    ),
    car_service: CarService = Depends(get_car_service),
    current_user: UserSchema = Depends(get_current_user),
) -> dict:
    result = await car_service.get_my_cars(
        page=page,
        limit=limit,
        sort_by=sort_by,
        order=order,
        allowed_sort_fields=[
            "created_at",
            "updated_at",
            "year",
            "make",
            "model",
        ],
        owner_uid=current_user.uid,
    )
    return ResponseSchema(detail="Success", result=result)


# Get a Car by id
@car_router.get(
    "/{car_uid}",
    response_model=ResponseSchema[CarSchema],
    response_model_exclude_none=True,
)
async def get_car_by_uid(
    car_uid: str = Path(min_length=32, max_length=36),
    car_service: CarService = Depends(get_car_service),
    current_user: UserSchema = Depends(get_current_user),
) -> dict:
    result = await car_service.get_car_with_owner_check(
        car_uid=car_uid, current_user=current_user
    )
    return ResponseSchema(detail="Success", result=result)


@car_router.post("/{car_uid}/owners", response_model=ResponseSchema[CarOwners])
async def add_owner(
    new_owner_uid: str,
    car_uid: str = Path(min_length=32, max_length=36),
    car_service: CarService = Depends(get_car_service),
    current_user: UserSchema = Depends(get_current_user),
) -> dict:
    result = await car_service.add_owner(
        car_uid=car_uid, new_owner_uid=new_owner_uid, current_user=current_user
    )
    return ResponseSchema(detail="Success", result=result)


@car_router.delete(
    "/{car_uid}/owners/{owner_uid}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_owner(
    delete_owner_uid: str,
    car_uid: str = Path(min_length=32, max_length=36),
    car_service: CarService = Depends(get_car_service),
    current_user: UserSchema = Depends(get_current_user),
):
    await car_service.delete_owner(
        car_uid=car_uid, delete_owner_uid=delete_owner_uid, current_user=current_user
    )
    return {}


# Update a Car data
@car_router.patch("/{car_uid}", response_model=ResponseSchema[CarSchema])
async def update_car(
    car_uid: str,
    car_update_data: CarUpdateSchema,
    car_service: CarService = Depends(get_car_service),
    current_user: UserSchema = Depends(get_current_user),
) -> dict:
    result = await car_service.update_car(
        car_uid=car_uid, car_data=car_update_data, current_user=current_user
    )
    return ResponseSchema(detail="Success", result=result)


# Delete a Car
@car_router.delete("/{car_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car(
    car_uid: str,
    car_service: CarService = Depends(get_car_service),
    current_user: UserSchema = Depends(get_current_user),
):
    await car_service.delete_car(car_uid=car_uid, current_user=current_user)
    return {}


# Get filtered Cars
@car_router.post(
    "/all",
    dependencies=[Depends(require_admin)],
    response_model=ResponseSchema[PageResponse[CarSchema]],
    response_model_exclude_none=True,
)
async def get_all_cars_by_filter(
    filter_schema: GetAllFilter, car_service: CarService = Depends(get_car_service)
):
    result = await car_service.filter_all_cars(filter_schema)
    return ResponseSchema(detail="Success", result=result)


# EXPENSES
# Create an Expense
@expenses_router.post(
    "/{car_uid}",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseSchema[ExpensesSchema],
)
async def create_expense(
    exp_data: ExpensesCreateSchema,
    car_uid: str = Path(min_length=32, max_length=36),
    expenses_service: ExpensesService = Depends(get_exp_service),
    current_user: UserSchema = Depends(get_current_user),
) -> dict:

    result = await expenses_service.create_expense(
        car_uid=car_uid, exp_data=exp_data, current_user=current_user
    )
    return ResponseSchema(detail="Success", result=result)


# Get single expense
@expenses_router.get(
    "/{car_uid}/expenses/{exp_uid}", response_model=ResponseSchema[ExpensesSchema]
)
async def get_single_expense(
    car_uid: str = Path(min_length=32, max_length=36),
    exp_uid: str = Path(min_length=32, max_length=36),
    expenses_service: ExpensesService = Depends(get_exp_service),
    current_user: UserSchema = Depends(get_current_user),
):
    result = await expenses_service.get_single_expense(
        car_uid=car_uid, exp_uid=exp_uid, current_user=current_user
    )
    return ResponseSchema(detail="Success", result=result)


# Udpate single expense
@expenses_router.patch(
    "/{car_uid}/expenses/{exp_uid}", response_model=ResponseSchema[ExpensesSchema]
)
async def update_single_expense(
    exp_update_data: ExpensesCreateSchema,
    car_uid: str = Path(min_length=32, max_length=36),
    exp_uid: str = Path(min_length=32, max_length=36),
    expenses_service: ExpensesService = Depends(get_exp_service),
    current_user: UserSchema = Depends(get_current_user),
):
    result = await expenses_service.update_single_expense(
        car_uid=car_uid,
        exp_uid=exp_uid,
        exp_update_data=exp_update_data,
        current_user=current_user,
    )
    return ResponseSchema(detail="Success", result=result)


# Delete single expense
@expenses_router.delete(
    "/{car_uid}/expenses/{exp_uid}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_single_expense(
    car_uid: str = Path(min_length=32, max_length=36),
    exp_uid: str = Path(min_length=32, max_length=36),
    expenses_service: ExpensesService = Depends(get_exp_service),
    current_user: UserSchema = Depends(get_current_user),
):
    await expenses_service.delete_single_expense(
        car_uid=car_uid, exp_uid=exp_uid, current_user=current_user
    )
    return {}


# Get all expenses for a single Car
@expenses_router.get(
    "/{car_uid}/expenses", response_model=ResponseSchema[PageResponse[ExpensesSchema]]
)
async def get_expenses_by_car_uid(
    car_uid: str = Path(min_length=32, max_length=36),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1),
    sort_by: str = Query(default="created_at", description="Поле сортировки"),
    order: str = Query(
        default="desc", pattern="^(asc|desc)$", description="Порядок сортировки"
    ),
    expenses_service: ExpensesService = Depends(get_exp_service),
    current_user: UserSchema = Depends(get_current_user),
):
    result = await expenses_service.get_expenses_by_car_uid(
        car_uid=car_uid,
        page=page,
        limit=limit,
        sort_by=sort_by,
        order=order,
        allowed_sort_fields=["created_at", "exp_summ", "name"],
        current_user=current_user,
    )
    return ResponseSchema(detail="Success", result=result)


# Delete all expenses for a single Car
@expenses_router.delete("/{car_uid}/expenses", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_expenses_by_car_uid(
    car_uid: str = Path(min_length=32, max_length=36),
    expenses_service: ExpensesService = Depends(get_exp_service),
    current_user: UserSchema = Depends(get_current_user),
):
    await expenses_service.delete_all_expenses_by_car_uid(
        car_uid=car_uid, current_user=current_user
    )
    return {}
