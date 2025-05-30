import math
from idlelib.iomenu import errors

from fastapi.exceptions import RequestValidationError
from sqlalchemy import delete, func
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession

from .schemas import (
    CarCreateSchema,
    CarUpdateSchema,
    ExpensesCreateSchema,
    PageResponse,
    GetAllFilter,
)
from sqlmodel import select, desc, asc
from .models import Cars, Expenses, MakesDirectory, ModelsDirectory


# Cars
class CarService:
    async def check_make(self, input_make: str, session: AsyncSession):
        statement = select(MakesDirectory).where(MakesDirectory.make == input_make)
        res = await session.exec(statement)
        make = res.first()
        if make:
            return make
        else:
            return None

    async def check_model(self, input_model: str, session: AsyncSession):
        statement = select(ModelsDirectory).where(ModelsDirectory.model == input_model)
        res = await session.exec(statement)
        model = res.first()
        print(model)
        if model:
            return model
        else:
            return None

    async def validate_make_model(
        self, car_data: CarCreateSchema, session: AsyncSession
    ):
        check_make = await self.check_make(car_data.make, session)
        check_model = await self.check_model(car_data.model, session)
        if not check_make or not check_model:
            errors = []
            if not check_make:
                errors.append(
                    {
                        "loc": ("make",),
                        "msg": "No such Make found in directory",
                        "type": "value_error",
                    }
                )
            if not check_model:
                errors.append(
                    {
                        "loc": ("model",),
                        "msg": "No such Model found in directory",
                        "type": "value_error",
                    }
                )
            raise RequestValidationError(errors)
        return car_data

    # Get single car
    async def get_car(self, car_uid: str, session: AsyncSession):
        statement = (
            select(Cars).options(selectinload(Cars.expenses)).where(Cars.uid == car_uid)
        )
        res = await session.exec(statement)
        car = res.first()
        if car is not None:
            return car
        else:
            return None

    # Get Cars filtered list
    async def filter_all_cars(
        self,
        search: GetAllFilter,
        session: AsyncSession,
    ):
        # Base query
        statement = select(Cars).options(selectinload(Cars.expenses))
        # Counting query
        count_statement = select(func.count(1)).select_from(Cars)

        # Filtering

        if search.make:
            statement = statement.filter_by(make=search.make)
            count_statement = count_statement.filter_by(make=search.make)
        if search.model:
            statement = statement.filter_by(model=search.model)
            count_statement = count_statement.filter_by(model=search.model)
        if search.prod_year:
            if search.prod_year.year_from:
                statement = statement.filter(Cars.year >= search.prod_year.year_from)
                count_statement = count_statement.filter(
                    Cars.year >= search.prod_year.year_from
                )
            if search.prod_year.year_to:
                statement = statement.filter(Cars.year <= search.prod_year.year_to)
                count_statement = count_statement.filter(
                    Cars.year <= search.prod_year.year_to
                )
        if search.status and search.status:
            statement = statement.filter_by(status=search.status)
            count_statement = count_statement.filter_by(status=search.status)

        # Sorting

        direction = desc if search.order_desc else asc
        if search.sort_by:
            statement = statement.order_by(direction(getattr(Cars, search.sort_by)))

        # Pagination

        offset_page = search.page - 1
        statement = statement.offset(offset_page * search.limit).limit(search.limit)

        # Counting records, pages

        total_records = (await session.exec(count_statement)).one() or 0
        total_pages = math.ceil(total_records / search.limit)

        # Executing query

        res = await session.exec(statement)
        result = res.unique().all()
        return PageResponse(
            page_number=search.page,
            page_size=search.limit,
            total_pages=total_pages,
            total_records=total_records,
            content=result,
        )

    # Create a Car
    async def create_car(self, car_data: CarCreateSchema, session: AsyncSession):
        await self.validate_make_model(car_data, session)
        new_expenses = []
        if car_data.expenses:
            new_expenses = [Expenses(**exp.model_dump()) for exp in car_data.expenses]
        new_car = Cars(
            **car_data.model_dump(exclude={"expenses"}), expenses=new_expenses
        )
        session.add(new_car)
        await session.commit()
        await session.refresh(new_car)
        return new_car

    # Update Car data
    async def update_car(
        self, car_uid: str, update_data: CarUpdateSchema, session: AsyncSession
    ):
        car_to_update = await self.get_car(car_uid, session)
        if car_to_update:
            update_data_dict = update_data.model_dump()
            for k, v in update_data_dict.items():
                setattr(car_to_update, k, v)
            await session.commit()
            await session.refresh(car_to_update)
            return car_to_update
        else:
            return None

    # Delete a Car
    async def delete_car(self, car_uid, session: AsyncSession):
        car_to_delete = await self.get_car(car_uid, session)
        if car_to_delete is not None:
            await session.delete(car_to_delete)
            await session.commit()
            return True
        else:
            return None


# Expenses
class ExpensesService:
    # Create an expense
    async def create_expense(
        self, car_uid: str, exp_data: ExpensesCreateSchema, session: AsyncSession
    ):
        car_update_service = CarService()
        car_to_update = await car_update_service.get_car(car_uid, session)
        if car_to_update:
            exp_data_dict = exp_data.model_dump()
            new_exp = Expenses(**exp_data_dict)
            new_exp.car_uid = car_uid

            session.add(new_exp)
            await session.commit()
            return new_exp
        else:
            return None

    # Get all expenses for a single car
    async def get_expenses(self, car_uid: str, session: AsyncSession):
        car_update_service = CarService()
        car_exists = await car_update_service.get_car(car_uid, session)
        if car_exists:
            statement = select(Expenses).where(Expenses.car_uid == car_uid)
            result = await session.exec(statement)
            exps = result.all()
            return exps
        else:
            return False

    # Delete all expenses for a single car
    async def delete_all_expenses_by_car_uid(self, car_uid: int, session: AsyncSession):
        car_update_service = CarService()
        car_exists = await car_update_service.get_car(car_uid, session)

        if not car_exists:
            return False
        statement = delete(Expenses).where(Expenses.car_uid == car_uid)
        await session.exec(statement)
        await session.commit()
        return True
