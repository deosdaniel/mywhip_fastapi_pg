import math
from itertools import count

from sqlalchemy import delete, func
from sqlalchemy.orm import joinedload, selectinload, load_only
from sqlmodel.ext.asyncio.session import AsyncSession
from typer.cli import state

from .schemas import (
    CarCreateSchema,
    CarUpdateSchema,
    ExpensesCreateSchema,
    PageResponse,
    GetAllSchema,
)
from sqlmodel import select, desc, asc, text
from .models import Cars, Expenses


"""Cars"""


class CarService:
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

    async def filter_all_cars(
        self,
        search: GetAllSchema,
        session: AsyncSession,
    ):
        # Base query
        statement = select(Cars).options(selectinload(Cars.expenses))
        # Counting query
        count_statement = select(func.count(1)).select_from(Cars)
        # Filtering

        if search.make:
            print("Make filter is not null")
            statement = statement.filter_by(make=search.make)
            count_statement = count_statement.filter_by(make=search.make)
        if search.model:
            print("Model filter is not null")
            statement = statement.filter_by(model=search.model)
            count_statement = count_statement.filter_by(model=search.model)
        if search.prod_year:
            print("Prod year filter is not null")
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
            print("Status filter is not null")
            statement = statement.filter_by(status=search.status)
            count_statement = count_statement.filter_by(status=search.status)
        # Sorting
        direction = desc if search.order_desc else asc
        if search.sort_by:
            print(f"search order is {direction}")
            statement = statement.order_by(direction(getattr(Cars, search.sort_by)))
        # Pagination
        offset_page = search.page - 1
        statement = statement.offset(offset_page * search.limit).limit(search.limit)
        # Counting records, pages
        total_records = (await session.exec(count_statement)).one() or 0
        total_pages = math.ceil(total_records / search.limit)

        res = await session.exec(statement)
        result = res.unique().all()
        return PageResponse(
            page_number=search.page,
            page_size=search.limit,
            total_pages=total_pages,
            total_records=total_records,
            content=result,
        )

    async def get_all_cars(self, session: AsyncSession, page: int = 1, limit: int = 0):
        """By defalut Cars list is sorted by created_at as newest -> oldest"""
        statement = (
            select(Cars)
            .options(selectinload(Cars.expenses))
            .order_by(desc(Cars.created_at))
        )

        # Pagination
        offset_page = page - 1
        statement = statement.offset(offset_page * limit).limit(limit)
        # Counting records, pages
        count_query = select(func.count(1)).select_from(Cars)
        total_record = (await session.exec(count_query)).one() or 0
        total_page = math.ceil(total_record / limit)

        res = await session.exec(statement)
        result = res.unique().all()
        return PageResponse(
            page_number=page,
            page_size=limit,
            total_pages=total_page,
            total_records=total_record,
            content=result,
        )

    async def create_car(self, car_data: CarCreateSchema, session: AsyncSession):
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

    async def delete_car(self, car_uid, session: AsyncSession):
        car_to_delete = await self.get_car(car_uid, session)
        if car_to_delete is not None:
            await session.delete(car_to_delete)
            await session.commit()
            return True
        else:
            return None


"""Expenses"""


class ExpensesService:

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

    async def delete_all_expenses_by_car_uid(self, car_uid: int, session: AsyncSession):
        car_update_service = CarService()
        car_exists = await car_update_service.get_car(car_uid, session)

        if not car_exists:
            return False
        statement = delete(Expenses).where(Expenses.car_uid == car_uid)
        await session.exec(statement)
        await session.commit()
        return True
