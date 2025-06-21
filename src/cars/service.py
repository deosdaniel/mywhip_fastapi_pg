import math
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from src.utils.schemas_common import PageResponse
from .models import Cars, Expenses
from .repositories import CarsRepository, ExpensesRepository
from .schemas import (
    CarCreateSchema,
    CarUpdateSchema,
    ExpensesCreateSchema,
    GetAllFilter,
)
from src.utils.exceptions import VinBusyException, EntityNotFoundException

from src.directories.service import DirectoryService
from ..users.schemas import UserSchema, UserRole
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
        await self.dir_service.validate_make_model(car_data.make, car_data.model)

        new_car_dict = car_data.model_dump()
        new_car_dict["make"] = car_data.make.lower().capitalize()
        new_car_dict["model"] = car_data.model.lower().capitalize()
        new_car_dict["owner_uid"] = owner_uid
        return await self.repository.create(table=Cars, new_entity_dict=new_car_dict)

    async def get_my_cars(
        self,
        page: int,
        limit: int,
        owner_uid: UUID,
        sort_by: str = "created_at",
        allowed_sort_fields: Optional[list[str]] = None,
        order: str = "desc",
    ):
        offset_page = (page - 1) * limit

        if allowed_sort_fields and sort_by not in allowed_sort_fields:
            raise HTTPException(
                status_code=400, detail=f"Sorting by '{sort_by}' is not allowed."
            )
        cars = await self.repository.get_my_cars(
            offset_page=offset_page,
            limit=limit,
            sort_by=sort_by,
            order=order,
            owner_uid=owner_uid,
        )

        total_records = await self.repository.count_my_cars(owner_uid)
        total_pages = math.ceil(total_records / limit)
        return PageResponse(
            page_number=page,
            page_size=limit,
            total_pages=total_pages,
            total_records=total_records,
            content=cars,
        )

    async def get_car_with_owner_check(self, car_uid: str, current_user: UserSchema):
        car = await self.get_by_uid(Cars, car_uid)
        if not car:
            raise EntityNotFoundException("car_uid")
        if current_user.role != UserRole.ADMIN and str(car.owner_uid) != str(
            current_user.uid
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )
        return car

    async def update_car(
        self, car_uid: UUID, car_data: CarUpdateSchema, current_user: UserSchema
    ) -> Cars:
        await self.get_car_with_owner_check(car_uid, current_user)
        return await self.update_by_uid(Cars, car_uid, car_data)

    async def delete_car(self, car_uid: UUID, current_user: UserSchema) -> None:
        await self.get_car_with_owner_check(car_uid, current_user)
        return await self.delete_by_uid(Cars, car_uid)

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
    async def create_expense(
        self, car_uid: UUID, exp_data: ExpensesCreateSchema, current_user: UserSchema
    ) -> Expenses:
        await self.car_service.get_car_with_owner_check(car_uid, current_user)
        exp_data_dict = exp_data.model_dump()
        new_exp = await self.repository.create_expense(car_uid, exp_data_dict)
        return new_exp

    # Get single expense
    async def get_single_expense(
        self, car_uid: UUID, exp_uid: str, current_user: UserSchema
    ) -> Expenses:
        await self.car_service.get_car_with_owner_check(car_uid, current_user)
        exp = await self.repository.get_single_exp(car_uid, exp_uid)
        if not exp:
            raise EntityNotFoundException("exp_uid")
        return exp

    # Update single expense
    async def update_single_expense(
        self,
        car_uid: UUID,
        exp_uid: UUID,
        exp_update_data: ExpensesCreateSchema,
        current_user: UserSchema,
    ) -> Expenses:
        await self.get_single_expense(car_uid, exp_uid, current_user)
        update_data_dict = exp_update_data.model_dump(exclude_unset=True)
        updated_exp = await self.repository.update_single_exp(
            car_uid, exp_uid, update_data_dict
        )
        return updated_exp

    # Delete single expense
    async def delete_single_expense(
        self,
        car_uid: UUID,
        exp_uid: UUID,
        current_user: UserSchema,
    ):
        await self.get_single_expense(car_uid, exp_uid, current_user)
        delete_exp = await self.repository.delete_single_exp(car_uid, exp_uid)
        if delete_exp:
            return True
        else:
            raise EntityNotFoundException("exp_uid")

    # Get all expenses for a single car
    async def get_expenses_by_car_uid(
        self,
        car_uid: UUID,
        current_user: UserSchema,
        page: int = 1,
        limit: int = 10,
        sort_by: str = "created_at",
        allowed_sort_fields: Optional[list[str]] = None,
        order: str = "desc",
    ) -> list[Expenses]:
        await self.car_service.get_car_with_owner_check(car_uid, current_user)

        offset_page = (page - 1) * limit

        if allowed_sort_fields and sort_by not in allowed_sort_fields:
            raise HTTPException(
                status_code=400, detail=f"Sorting by '{sort_by}' is not allowed."
            )
        expenses = await self.repository.get_exp_by_car_uid(
            car_uid=car_uid,
            offset_page=offset_page,
            limit=limit,
            sort_by=sort_by,
            order=order,
        )

        total_records = await self.repository.count_exp_by_car_uid(car_uid)
        total_pages = math.ceil(total_records / limit)

        return PageResponse(
            page_number=page,
            page_size=limit,
            total_pages=total_pages,
            total_records=total_records,
            content=expenses,
        )

    # Delete all expenses for a single car
    async def delete_all_expenses_by_car_uid(
        self, car_uid: UUID, current_user: UserSchema
    ) -> None:
        await self.get_expenses_by_car_uid(car_uid, current_user)
        await self.repository.delete_exp_by_car_uid(car_uid)
        return True
