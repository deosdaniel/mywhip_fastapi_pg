import math
from uuid import UUID
from src.utils.schemas_common import PageResponse
from .models import Cars
from .repositories import CarsRepository, ExpensesRepository
from .schemas import (
    CarCreateSchema,
    CarUpdateSchema,
    ExpensesCreateSchema,
    GetAllFilter,
)
from src.utils.exceptions import VinBusyException, EntityNotFoundException

from src.directories.service import DirectoryService
from ..utils.base_service_repo import BaseService


# Cars
class CarService(BaseService[CarsRepository]):
    # Add car_service to have access to it's methods
    def __init__(self, repository: CarsRepository, dir_service: DirectoryService):
        super().__init__(repository)
        self.dir_service = dir_service

    # Create a Car
    async def create_car(
        self,
        car_data: CarCreateSchema,
        owner_uid: UUID,
    ):
        vin_collision = await self.repository.check_vin_collision(car_data.vin)
        if vin_collision:
            raise VinBusyException
        make = await self.dir_service.get_single_make(car_data.make)
        model = await self.dir_service.get_single_model_by_make(
            car_data.model, make.uid
        )
        print(f"make {make} model {model}")
        new_car_dict = car_data.model_dump()
        new_car_dict["make"] = car_data.make
        new_car_dict["model"] = car_data.model
        new_car_dict["owner_uid"] = owner_uid
        return await self.repository.create(table=Cars, new_entity_dict=new_car_dict)

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


# Expenses
class ExpensesService(BaseService[ExpensesRepository]):
    # Add car_service to have access to it's methods
    def __init__(self, repository: ExpensesRepository, car_service: CarService):
        super().__init__(repository)
        self.car_service = car_service

    # Create an expense
    async def create_expense(self, car_uid: str, exp_data: ExpensesCreateSchema):
        car = await self.get_by_uid(Cars, car_uid)
        exp_data_dict = exp_data.model_dump()
        new_exp = await self.repository.create_expense(car_uid, exp_data_dict)
        return new_exp

    # Get single expense
    async def get_single_expense(self, car_uid: str, exp_uid: str):
        await self.get_by_uid(Cars, car_uid)
        exp = await self.repository.get_single_exp(car_uid, exp_uid)
        if not exp:
            raise EntityNotFoundException("exp_uid")
        return exp

    # Get all expenses for a single car
    async def get_expenses_by_car_uid(
        self, car_uid: str, page: int = 1, limit: int = 10
    ):
        await self.get_by_uid(Cars, car_uid)

        offset_page = (page - 1) * limit

        expenses = await self.repository.get_exp_by_car_uid(car_uid, offset_page, limit)

        total_records = await self.repository.count_exp_by_car_uid(car_uid)
        total_pages = math.ceil(total_records / limit)

        return PageResponse(
            page_number=page,
            page_size=limit,
            total_pages=total_pages,
            total_records=total_records,
            content=expenses,
        )

    # Update single expense
    async def update_single_expense(
        self,
        car_uid: str,
        exp_uid: str,
        exp_update_data: ExpensesCreateSchema,
    ):
        await self.get_single_expense(car_uid, exp_uid)
        update_data_dict = exp_update_data.model_dump(exclude_unset=True)
        updated_exp = await self.repository.update_single_exp(
            car_uid, exp_uid, update_data_dict
        )

        return updated_exp

    # Delete single expense
    async def delete_single_expense(
        self,
        car_uid: str,
        exp_uid: str,
    ):
        await self.get_single_expense(car_uid, exp_uid)
        delete_exp = await self.repository.delete_single_exp(car_uid, exp_uid)
        if delete_exp:
            return True
        else:
            raise EntityNotFoundException("exp_uid")

    # Delete all expenses for a single car
    async def delete_all_expenses_by_car_uid(self, car_uid: str):
        await self.get_expenses_by_car_uid(car_uid)
        await self.repository.delete_exp_by_car_uid(car_uid)
        return True
