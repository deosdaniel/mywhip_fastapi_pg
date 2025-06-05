import math
from uuid import UUID

from sqlalchemy import delete, func
from sqlalchemy.orm import selectinload
from src.utils.schemas_common import PageResponse
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
from ..utils.base_service import BaseService


# Cars
class CarService(BaseService):
    # Create a Car
    async def create_car(self, car_data: CarCreateSchema, owner_uid: UUID):
        statement = (
            select(Cars).where(Cars.vin == car_data.vin).where(Cars.status != "SOLD")
        )
        check_vin = await self.session.exec(statement)
        check_vin = check_vin.first()
        if check_vin is None:
            directory_service = DirectoryService(self.session)
            validate_make = await directory_service.get_makes(
                page=None, limit=None, requested_make=car_data.make
            )
            validate_model = await directory_service.get_models(
                page=None, limit=None, requested_model=car_data.model
            )
            new_expenses = []
            if car_data.expenses:
                new_expenses = [
                    Expenses(**exp.model_dump()) for exp in car_data.expenses
                ]
            new_car = Cars(
                **car_data.model_dump(exclude={"make", "model", "expenses"}),
                make=validate_make.make,
                model=validate_model.model,
                expenses=new_expenses,
                owner_uid=owner_uid
            )
            self.session.add(new_car)
            await self.session.commit()
            await self.session.refresh(new_car)
            return new_car
        else:
            raise VinBusyException()

    # Get single car
    async def get_car(self, car_uid: str):
        statement = (
            select(Cars).options(selectinload(Cars.expenses)).where(Cars.uid == car_uid)
        )
        res = await self.session.exec(statement)
        car = res.first()
        if car:
            return car
        else:
            raise EntityNotFoundException("car_uid")

    # Get Cars filtered list
    async def filter_all_cars(
        self,
        filter_schema: GetAllFilter,
    ):
        # Base query
        statement = select(Cars).options(selectinload(Cars.expenses))
        # Counting query
        count_statement = select(func.count(1)).select_from(Cars)
        # Filtering
        if filter_schema.make:
            statement = statement.filter_by(make=filter_schema.make)
            count_statement = count_statement.filter_by(make=filter_schema.make)
        if filter_schema.model:
            statement = statement.filter_by(model=filter_schema.model)
            count_statement = count_statement.filter_by(model=filter_schema.model)
        if filter_schema.prod_year:
            if filter_schema.prod_year.year_from:
                statement = statement.filter(
                    Cars.year >= filter_schema.prod_year.year_from
                )
                count_statement = count_statement.filter(
                    Cars.year >= filter_schema.prod_year.year_from
                )
            if filter_schema.prod_year.year_to:
                statement = statement.filter(
                    Cars.year <= filter_schema.prod_year.year_to
                )
                count_statement = count_statement.filter(
                    Cars.year <= filter_schema.prod_year.year_to
                )
        if filter_schema.status and filter_schema.status:
            statement = statement.filter_by(status=filter_schema.status)
            count_statement = count_statement.filter_by(status=filter_schema.status)
        # Sorting
        direction = desc if filter_schema.order_desc else asc
        if filter_schema.sort_by:
            statement = statement.order_by(
                direction(getattr(Cars, filter_schema.sort_by))
            )
        # Pagination
        offset_page = filter_schema.page - 1
        statement = statement.offset(offset_page * filter_schema.limit).limit(
            filter_schema.limit
        )
        # Counting records, pages
        total_records = (await self.session.exec(count_statement)).one() or 0
        total_pages = math.ceil(total_records / filter_schema.limit)
        # Executing query
        res = await self.session.exec(statement)
        result = res.unique().all()
        return PageResponse(
            page_number=filter_schema.page,
            page_size=filter_schema.limit,
            total_pages=total_pages,
            total_records=total_records,
            content=result,
        )

    # Update Car data
    async def update_car(self, car_uid: str, update_data: CarUpdateSchema):
        car_to_update = await self.get_car(car_uid)
        update_data_dict = update_data.model_dump()
        for k, v in update_data_dict.items():
            setattr(car_to_update, k, v)
        await self.session.commit()
        await self.session.refresh(car_to_update)
        return car_to_update

    # Delete a Car
    async def delete_car(self, car_uid):
        car_to_delete = await self.get_car(car_uid)
        await self.session.delete(car_to_delete)
        await self.session.commit()
        return True


# Expenses
class ExpensesService(BaseService):
    # Create an expense
    async def create_expense(self, car_uid: str, exp_data: ExpensesCreateSchema):
        car_update_service = CarService(self.session)
        await car_update_service.get_car(car_uid)

        exp_data_dict = exp_data.model_dump()
        new_exp = Expenses(**exp_data_dict)
        new_exp.car_uid = car_uid
        self.session.add(new_exp)
        await self.session.commit()
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
