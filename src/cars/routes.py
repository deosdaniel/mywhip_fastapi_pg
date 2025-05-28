from fastapi import APIRouter, status, Depends, Query, Path
from fastapi.exceptions import HTTPException
from typing import List

from src.cars.schemas import (
    CarUpdateSchema,
    CarCreateSchema,
    ExpensesSchema,
    ExpensesCreateSchema,
    CarSchema,
    ResponseSchema,
    PageResponse,
    GetAllFilter,
)
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.cars.service import CarService, ExpensesService


car_router = APIRouter()

car_service = CarService()
expenses_service = ExpensesService()


# Get a Car by id
@car_router.get(
    "/{car_uid}", response_model=CarSchema, response_model_exclude_none=True
)
async def get_car(
    car_uid: str = Path(min_length=32, max_length=36),
    session: AsyncSession = Depends(get_session),
) -> dict:
    car = await car_service.get_car(car_uid, session)
    if car:
        return car
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Car not found"
        )


# Get filtered Cars
@car_router.post(
    "/filter",
    response_model=ResponseSchema[PageResponse[CarSchema]],
    response_model_exclude_none=True,
)
async def filter_all_cars(
    search: GetAllFilter,
    session: AsyncSession = Depends(get_session),
):
    cars = await car_service.filter_all_cars(search, session)
    return ResponseSchema(detail="Success", result=cars)


# Create a Car
@car_router.post("/", status_code=status.HTTP_201_CREATED, response_model=CarSchema)
async def create_car(
    car_data: CarCreateSchema, session: AsyncSession = Depends(get_session)
) -> dict:
    new_car = await car_service.create_car(car_data, session)
    return new_car


# Update a Car data
@car_router.patch("/{car_uid}", response_model=CarSchema)
async def update_car(
    car_uid: str,
    car_update_data: CarUpdateSchema,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_car = await car_service.update_car(car_uid, car_update_data, session)

    if not updated_car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot update, car does not exist",
        )
    else:
        return updated_car


# Delete a Car
@car_router.delete("/{car_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car(car_uid: str, session: AsyncSession = Depends(get_session)):

    car_to_delete = await car_service.delete_car(car_uid, session)

    if car_to_delete:
        return {}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot delete, car does not exist",
        )


# EXPENSES
# Create an Expense
@car_router.post(
    "/{car_uid}", status_code=status.HTTP_201_CREATED, response_model=ExpensesSchema
)
async def create_expense(
    car_uid: str,
    exp_data: ExpensesCreateSchema,
    session: AsyncSession = Depends(get_session),
) -> dict:

    result = await expenses_service.create_expense(car_uid, exp_data, session)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Car does not exist"
        )


# Get all expenses for a single Car
@car_router.get("/{car_uid}/expenses", response_model=List[ExpensesSchema])
async def get_expenses_by_car_uid(
    car_uid: str, session: AsyncSession = Depends(get_session)
):
    result = await expenses_service.get_expenses(car_uid, session)
    if result:
        return result
    elif result is False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Car not found"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No expenses yet"
        )


# Delete all expenses for a single Car
@car_router.delete("/{car_uid}/expenses", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_expenses_by_car_uid(
    car_uid: str, session: AsyncSession = Depends(get_session)
):
    result = await expenses_service.delete_all_expenses_by_car_uid(car_uid, session)

    if result:
        return {}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Car not found"
        )
