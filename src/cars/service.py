import math

from sqlalchemy import delete, func
from src.utils.schemas_common import PageResponse
from .repositories import CarsRepository, ExpensesRepository
from .schemas import (
    CarCreateSchema,
    CarUpdateSchema,
    ExpensesCreateSchema,
    GetAllFilter,
)
from sqlmodel import select, desc, asc
from .models import Cars, Expenses
from src.utils.exceptions import VinBusyException, EntityNotFoundException

from src.directories.service import DirectoryService
from ..directories.repositories import DirectoryRepository
from ..utils.base_service_repo import BaseService


# Cars
class CarService(BaseService[CarsRepository]):
    # Create a Car
    async def create_car(
        self,
        car_data: CarCreateSchema,
        # owner_uid: UUID,
    ):
        if await self.repository.check_vin_collision(car_data.vin):
            raise VinBusyException()

        # await DirectoryRepository.get_single_make(self, car_data.make)
        # await DirectoryRepository.get_single_model(self, car_data.model)

        new_car_dict = car_data.model_dump()
        new_car_dict["make"] = car_data.make
        new_car_dict["model"] = car_data.model
        # new_car_dict["owner_uid"] = owner_uid
        return await self.repository.create_car(new_car_dict)

    # Get single car
    async def get_car_by_uid(self, car_uid: str):

        car = await self.repository.get_car_by_uid(car_uid)
        if car:
            return car
        else:
            raise EntityNotFoundException("car_uid")

    # Get Cars filtered list
    async def filter_all_cars(
        self,
        filter_schema: GetAllFilter,
    ):

        offset_page = (filter_schema.page - 1) * filter_schema.limit

        cars = await self.repository.get_cars_filtered(offset_page, filter_schema)

        total_records = await self.repository.count_filtered_records(filter_schema)
        total_pages = math.ceil(total_records / filter_schema.limit)
        return PageResponse(
            page_number=filter_schema.page,
            page_size=filter_schema.limit,
            total_pages=total_pages,
            total_records=total_records,
            content=cars,
        )

    # Update Car data
    async def update_car(self, car_uid: str, update_data: CarUpdateSchema):
        update_dict = update_data.model_dump(exclude_unset=True)
        updated_car = await self.repository.update_car(car_uid, update_dict)
        if not updated_car:
            raise EntityNotFoundException("car_uid")
        return updated_car

    # Delete a Car
    async def delete_car(self, car_uid):
        delete_car = await self.repository.delete_car(car_uid)
        if not delete_car:
            raise EntityNotFoundException("car_uid")
        return True


# Expenses
class ExpensesService(BaseService[ExpensesRepository]):
    def __init__(self, repository: ExpensesRepository, car_service: CarService):
        super().__init__(repository)
        self.car_service = car_service

    # Create an expense
    async def create_expense(self, car_uid: str, exp_data: ExpensesCreateSchema):
        car = await self.car_service.get_car_by_uid(car_uid)
        exp_data_dict = exp_data.model_dump()
        new_exp = await self.repository.create_expense(car_uid, exp_data_dict)
        return new_exp

    # Get single expense
    async def get_single_expense(self, car_uid: str, exp_uid: str):
        car_update_service = CarService(self.session)
        await car_update_service.get_car(car_uid)
        statement = (
            select(Expenses)
            .where(Expenses.car_uid == car_uid)
            .where(Expenses.uid == exp_uid)
        )
        result = await self.session.exec(statement)
        exp = result.first()
        if exp:
            return exp
        else:
            raise EntityNotFoundException("exp_uid")

    # Get all expenses for a single car
    async def get_expenses_by_car_uid(
        self, car_uid: str, page: int = 1, limit: int = 10
    ):
        car_update_service = CarService(self.session)
        await car_update_service.get_car(car_uid)
        statement = select(Expenses).where(Expenses.car_uid == car_uid)
        # Pagination
        offset_page = page - 1
        statement = statement.offset(offset_page * limit).limit(limit)
        # Counting records, pages
        count_statement = (
            select(func.count(1))
            .select_from(Expenses)
            .where(Expenses.car_uid == car_uid)
        )
        total_records = (await self.session.exec(count_statement)).one() or 0
        total_pages = math.ceil(total_records / limit)
        result = await self.session.exec(statement)
        result = result.all()
        return PageResponse(
            page_number=page,
            page_size=limit,
            total_pages=total_pages,
            total_records=total_records,
            content=result,
        )

    # Update single expense
    async def update_single_expense(
        self,
        car_uid: str,
        exp_uid: str,
        exp_update_data: ExpensesCreateSchema,
    ):
        expense_to_update = await self.get_single_expense(car_uid, exp_uid)
        update_data_dict = exp_update_data.model_dump()
        for k, v in update_data_dict.items():
            setattr(expense_to_update, k, v)
        await self.session.commit()
        await self.session.refresh(expense_to_update)
        return expense_to_update

    # Delete single expense
    async def delete_single_expense(
        self,
        car_uid: str,
        exp_uid: str,
    ):
        expense_to_delete = await self.get_single_expense(car_uid, exp_uid)
        await self.session.delete(expense_to_delete)
        await self.session.commit()
        return True

    # Delete all expenses for a single car
    async def delete_all_expenses_by_car_uid(self, car_uid: str):
        car_update_service = CarService(self.session)
        await car_update_service.get_car(car_uid)
        statement = delete(Expenses).where(Expenses.car_uid == car_uid)
        await self.session.exec(statement)
        await self.session.commit()
        return True
