from fastapi import APIRouter, status, Depends, Query, Path
from fastapi.exceptions import HTTPException, RequestValidationError
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.cars.service import CarService, ExpensesService, DirectoryService
from src.cars.schemas import (
    CarUpdateSchema,
    CarCreateSchema,
    ExpensesSchema,
    ExpensesCreateSchema,
    CarSchema,
    ResponseSchema,
    PageResponse,
    GetAllFilter,
    MakeSchema,
    ModelSchema,
)

car_router = APIRouter()
expenses_router = APIRouter()
directory_router = APIRouter()

car_service = CarService()
expenses_service = ExpensesService()
directory_service = DirectoryService()


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
    "/all",
    response_model=ResponseSchema[PageResponse[CarSchema]],
    response_model_exclude_none=True,
)
async def get_all_cars_by_filter(
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
@expenses_router.post(
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


# Get single expense
@expenses_router.get(
    "/{car_uid}/expenses/{exp_uid}", response_model=List[ExpensesSchema]
)
async def get_single_expense(
    car_uid: str, exp_uid: str, session: AsyncSession = Depends(get_session)
):
    result = await expenses_service.get_single_expense(car_uid, exp_uid, session)
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


# Get all expenses for a single Car
@expenses_router.get("/{car_uid}/expenses", response_model=List[ExpensesSchema])
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


# Udpate single expense
@expenses_router.patch(
    "/{car_uid}/expenses/{exp_uid}", response_model=List[ExpensesSchema]
)
async def update_single_expense(
    car_uid: str,
    exp_uid: str,
    exp_update_data: ExpensesCreateSchema,
    session: AsyncSession = Depends(get_session),
):
    result = await expenses_service.update_single_expense(
        car_uid, exp_uid, exp_update_data, session
    )
    if result:
        return result
    else:  # ????? Where do I raise exceptions? here or in service layer? How to raise different details?
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="????????")


# Delete all expenses for a single Car
@expenses_router.delete("/{car_uid}/expenses", status_code=status.HTTP_204_NO_CONTENT)
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


# Delete single expense
@expenses_router.delete(
    "/{car_uid}/expenses/{exp_uid}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_single_expense(
    car_uid: str, exp_uid: str, session: AsyncSession = Depends(get_session)
):

    result = await expenses_service.delete_single_expense(car_uid, exp_uid, session)
    # REWRITE LOGIC BELOW TO RAISE VALID ERRORS FOR EXP/CAR NOT FOUND
    if result:  # redo
        return {}  # redo
    else:  # redo
        raise HTTPException(  # redo
            status_code=status.HTTP_404_NOT_FOUND, detail="Car not found"  # redo
        )  # redo


# DIRECTORIES
@directory_router.get(
    "/makes",
    response_model=ResponseSchema[PageResponse[MakeSchema]]
    | ResponseSchema[MakeSchema],
)
async def get_makes(
    session: AsyncSession = Depends(get_session),
    page: int | None = 1,
    limit: int | None = 10,
    requested_make: str | None = None,
):
    result = await directory_service.get_makes(session, page, limit, requested_make)
    return ResponseSchema(detail="Success", result=result)


@directory_router.get(
    "/models",
    response_model=ResponseSchema[PageResponse[ModelSchema]]
    | ResponseSchema[ModelSchema],
)
async def get_models(
    session: AsyncSession = Depends(get_session),
    page: int = 1,
    limit: int = 10,
    requested_model: str | None = None,
):
    result = await directory_service.get_models(session, page, limit, requested_model)
    return ResponseSchema(detail="Success", result=result)
