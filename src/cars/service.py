import math

from fastapi.exceptions import RequestValidationError, HTTPException
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


def raise_item_not_found_exception(item: str):
    return HTTPException(status_code=404, detail=f"Sorry, {item} not found")


# Cars
class CarService:
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
            return None  # INSTEAD RAISE 404 ERROR - CAR NOT FOUND

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
        directory_service = DirectoryService()
        validate_make = await directory_service.get_makes(
            session, page=None, limit=None, requested_make=car_data.make
        )
        validate_model = await directory_service.get_models(
            session, page=None, limit=None, requested_model=car_data.model
        )
        new_expenses = []
        if car_data.expenses:
            new_expenses = [Expenses(**exp.model_dump()) for exp in car_data.expenses]
        new_car = Cars(
            **car_data.model_dump(exclude={"make", "model", "expenses"}),
            make=validate_make.make,
            model=validate_model.model,
            expenses=new_expenses,
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
        if (
            car_to_update
        ):  # MAYBE THIS "IF" IS NOT NECESSARY IN CASE OF CHECKING FOR 404 IN SELF.GET_CAR??
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
        if (
            car_to_delete is not None
        ):  # MAYBE THIS "IF" IS NOT NECESSARY IN CASE OF CHECKING FOR 404 IN SELF.GET_CAR??
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
        if (
            car_to_update
        ):  # MAYBE THIS "IF" IS NOT NECESSARY IN CASE OF CHECKING FOR 404 IN SELF.GET_CAR??
            exp_data_dict = exp_data.model_dump()
            new_exp = Expenses(**exp_data_dict)
            new_exp.car_uid = car_uid

            session.add(new_exp)
            await session.commit()
            return new_exp
        else:
            return None

    # Get single expense
    async def get_single_expense(
        self, car_uid: str, exp_uid: str, session: AsyncSession
    ):
        car_update_service = CarService()
        car_exists = await car_update_service.get_car(car_uid, session)
        if (
            car_exists
        ):  # MAYBE THIS "IF" IS NOT NECESSARY IN CASE OF CHECKING FOR 404 IN SELF.GET_CAR??
            statement = (
                select(Expenses)
                .where(Expenses.car_uid == car_uid)
                .where(Expenses.uid == exp_uid)
            )
            result = await session.exec(statement)
            exp = result.first()
            if not exp:
                return None  # INSTEAD RAISE 404 ERROR - EXPENSE NOT FOUND
            else:
                return exp
        else:
            return False  # MAYBE THIS IS NOT NECESSARY

    # Get all expenses for a single car
    async def get_expenses_by_car_uid(
        self, car_uid: str, session: AsyncSession, page: int = 1, limit: int = 10
    ):
        car_update_service = CarService()
        car_exists = await car_update_service.get_car(car_uid, session)
        if (
            car_exists
        ):  # MAYBE THIS "IF" IS NOT NECESSARY IN CASE OF CHECKING FOR 404 IN SELF.GET_CAR??
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
            total_records = (await session.exec(count_statement)).one() or 0
            total_pages = math.ceil(total_records / limit)

            result = await session.exec(statement)
            result = result.all()
            if result:

                return PageResponse(
                    page_number=page,
                    page_size=limit,
                    total_pages=total_pages,
                    total_records=total_records,
                    content=result,
                )
            return None
        else:
            return False  # MAYBE THIS IS NOT NECESSARY

    # Update single expense
    async def update_single_expense(
        self,
        car_uid: str,
        exp_uid: str,
        exp_update_data: ExpensesCreateSchema,
        session: AsyncSession,
    ):

        expense_to_update = await self.get_single_expense(car_uid, exp_uid, session)
        if (
            expense_to_update
        ):  # MAYBE THIS "IF" IS NOT NECESSARY IN CASE OF CHECKING FOR 404 IN SELF.GET_SINGLE_EXPENSE??
            update_data_dict = exp_update_data.model_dump()
            for k, v in update_data_dict.items():
                setattr(expense_to_update, k, v)
            await session.commit()
            await session.refresh(expense_to_update)
            return expense_to_update
        elif expense_to_update is False:
            return False  # MAYBE THIS IS NOT NECESSARY
        else:
            return None  # MAYBE THIS IS NOT NECESSARY

    # Delete single expense
    async def delete_single_expense(
        self, car_uid: str, exp_uid: str, session: AsyncSession
    ):
        expense_to_delete = await self.get_single_expense(car_uid, exp_uid, session)
        if (
            expense_to_delete
        ):  # MAYBE THIS "IF" IS NOT NECESSARY IN CASE OF CHECKING FOR 404 IN SELF.GET_SINGLE_EXPENSE??
            await session.delete(expense_to_delete)
            await session.commit()
            return True
        elif expense_to_delete is False:
            return False  # MAYBE THIS IS NOT NECESSARY
        else:
            return None  # MAYBE THIS IS NOT NECESSARY

    # Delete all expenses for a single car
    async def delete_all_expenses_by_car_uid(self, car_uid: str, session: AsyncSession):
        car_update_service = CarService()
        car_exists = await car_update_service.get_car(car_uid, session)

        if (
            not car_exists
        ):  # MAYBE THIS "IF" IS NOT NECESSARY IN CASE OF CHECKING FOR 404 IN SELF.GET_CAR??
            return False
        statement = delete(Expenses).where(Expenses.car_uid == car_uid)
        await session.exec(statement)
        await session.commit()
        return True


class DirectoryService:
    async def get_makes(
        self,
        session: AsyncSession,
        page: int = None,
        limit: int = None,
        requested_make: str = None,
    ):
        if requested_make:
            statement = select(MakesDirectory).where(
                func.lower(MakesDirectory.make) == func.lower(requested_make)
            )
            result = await session.exec(statement)
            result = result.first()
            if not result or result == "null":
                raise RequestValidationError(
                    {
                        "loc": ("requested_make",),
                        "msg": "No such Make found in directory",
                        "type": "value_error",
                    }
                )
            return result
        else:
            statement = select(MakesDirectory)

            # Pagination
            offset_page = page - 1
            statement = statement.offset(offset_page * limit).limit(limit)

            # Counting records, pages
            count_statement = select(func.count(1)).select_from(MakesDirectory)
            total_records = (await session.exec(count_statement)).one() or 0
            total_pages = math.ceil(total_records / limit)

            result = await session.exec(statement)
            result = result.all()
            return PageResponse(
                page_number=page,
                page_size=limit,
                total_pages=total_pages,
                total_records=total_records,
                content=result,
            )

    async def get_models(
        self,
        session: AsyncSession,
        page: int | None,
        limit: int | None,
        requested_model: str = None,
    ):
        if requested_model:
            statement = select(ModelsDirectory).where(
                func.lower(ModelsDirectory.model) == func.lower(requested_model)
            )
            result = await session.exec(statement)
            result = result.first()
            if not result or result == "null":
                raise RequestValidationError(
                    {
                        "loc": ("requested_model",),
                        "msg": "No such Model found in directory",
                        "type": "value_error",
                    }
                )
            return result
        else:
            statement = select(ModelsDirectory)

            # Pagination
            offset_page = page - 1
            statement = statement.offset(offset_page * limit).limit(limit)

            # Counting records, pages
            count_statement = select(func.count(1)).select_from(ModelsDirectory)
            total_records = (await session.exec(count_statement)).one() or 0
            total_pages = math.ceil(total_records / limit)

            result = await session.exec(statement)
            result = result.all()
            print(f"Я отдаю список")
            return PageResponse(
                page_number=page,
                page_size=limit,
                total_pages=total_pages,
                total_records=total_records,
                content=result,
            )
