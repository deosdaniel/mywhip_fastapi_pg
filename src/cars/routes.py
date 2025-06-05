from fastapi import APIRouter, status, Path
from src.db.main import db_session
from src.cars.service import CarService, ExpensesService
from src.utils.schemas_common import ResponseSchema, PageResponse
from src.cars.schemas import (
    CarUpdateSchema,
    CarCreateSchema,
    ExpensesSchema,
    ExpensesCreateSchema,
    CarSchema,
    GetAllFilter,
)

car_router = APIRouter()
expenses_router = APIRouter()


car_service = CarService()
expenses_service = ExpensesService()


# Create a Car
@car_router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=ResponseSchema[CarSchema]
)
async def create_car(session: db_session, car_data: CarCreateSchema) -> dict:
    result = await car_service.create_car(car_data, session)
    return ResponseSchema(detail="Success", result=result)


# Get a Car by id
@car_router.get(
    "/{car_uid}",
    response_model=ResponseSchema[CarSchema],
    response_model_exclude_none=True,
)
async def get_car(
    session: db_session,
    car_uid: str = Path(min_length=32, max_length=36),
) -> dict:
    result = await car_service.get_car(car_uid, session)
    return ResponseSchema(detail="Success", result=result)


# Get filtered Cars
@car_router.post(
    "/all",
    response_model=ResponseSchema[PageResponse[CarSchema]],
    response_model_exclude_none=True,
)
async def get_all_cars_by_filter(session: db_session, filter_schema: GetAllFilter):
    result = await car_service.filter_all_cars(filter_schema, session)
    return ResponseSchema(detail="Success", result=result)


# Update a Car data
@car_router.patch("/{car_uid}", response_model=ResponseSchema[CarSchema])
async def update_car(
    session: db_session, car_uid: str, car_update_data: CarUpdateSchema
) -> dict:
    result = await car_service.update_car(car_uid, car_update_data, session)
    return ResponseSchema(detail="Success", result=result)


# Delete a Car
@car_router.delete("/{car_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car(car_uid: str, session: db_session):

    await car_service.delete_car(car_uid, session)
    return {}


# EXPENSES
# Create an Expense
@expenses_router.post(
    "/{car_uid}",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseSchema[ExpensesSchema],
)
async def create_expense(
    session: db_session,
    exp_data: ExpensesCreateSchema,
    car_uid: str = Path(min_length=32, max_length=36),
) -> dict:

    result = await expenses_service.create_expense(car_uid, exp_data, session)
    return ResponseSchema(detail="Success", result=result)


# Get single expense
@expenses_router.get(
    "/{car_uid}/expenses/{exp_uid}", response_model=ResponseSchema[ExpensesSchema]
)
async def get_single_expense(
    session: db_session,
    car_uid: str = Path(min_length=32, max_length=36),
    exp_uid: str = Path(min_length=32, max_length=36),
):
    result = await expenses_service.get_single_expense(car_uid, exp_uid, session)
    return ResponseSchema(detail="Success", result=result)


# Get all expenses for a single Car
@expenses_router.get(
    "/{car_uid}/expenses", response_model=ResponseSchema[PageResponse[ExpensesSchema]]
)
async def get_expenses_by_car_uid(
    session: db_session,
    car_uid: str = Path(min_length=32, max_length=36),
    page: int = 1,
    limit: int = 10,
):
    result = await expenses_service.get_expenses_by_car_uid(
        car_uid, session, page, limit
    )
    return ResponseSchema(detail="Success", result=result)


# Udpate single expense
@expenses_router.patch(
    "/{car_uid}/expenses/{exp_uid}", response_model=ResponseSchema[ExpensesSchema]
)
async def update_single_expense(
    session: db_session,
    exp_update_data: ExpensesCreateSchema,
    car_uid: str = Path(min_length=32, max_length=36),
    exp_uid: str = Path(min_length=32, max_length=36),
):
    result = await expenses_service.update_single_expense(
        car_uid, exp_uid, exp_update_data, session
    )
    return ResponseSchema(detail="Success", result=result)


# Delete single expense
@expenses_router.delete(
    "/{car_uid}/expenses/{exp_uid}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_single_expense(
    session: db_session,
    car_uid: str = Path(min_length=32, max_length=36),
    exp_uid: str = Path(min_length=32, max_length=36),
):
    await expenses_service.delete_single_expense(car_uid, exp_uid, session)
    return {}


# Delete all expenses for a single Car
@expenses_router.delete("/{car_uid}/expenses", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_expenses_by_car_uid(
    session: db_session,
    car_uid: str = Path(min_length=32, max_length=36),
):
    await expenses_service.delete_all_expenses_by_car_uid(car_uid, session)
    return {}
