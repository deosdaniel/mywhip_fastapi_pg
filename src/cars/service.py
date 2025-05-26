import math
from sqlalchemy import delete, func
from sqlalchemy.orm import joinedload, selectinload, load_only
from sqlalchemy.sql.operators import is_, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import CarCreateSchema, CarUpdateSchema, ExpensesSchema, ExpensesCreateSchema, CarStatusChoices, \
    PageResponse
from sqlmodel import select, desc, asc, text
from .models import Cars, Expenses


"""Cars"""
class CarService:
    async def get_car(self, car_uid: str, session: AsyncSession):
        statement = select(Cars).options(selectinload(Cars.expenses)).where(Cars.uid == car_uid)
        res = await session.exec(statement)
        car = res.first()
        if car is not None:
            return car
        else:
            return None

    async def get_all_cars(
            self,
            session: AsyncSession,
            page: int = 1,
            limit: int = 0,
            columns: str = None,
            sort: str = None,
            filter_by: str = None
    ):
        """By defalut Cars list is sorted by created_at as newest -> oldest"""
        statement = select(Cars).options(selectinload(Cars.expenses))

        """columns in fastapi query look like : make-model-vin..."""
        if columns is not None and columns !='all':
            new_columns = columns.split('-')

            column_list = []
            for data in new_columns:
                column_list.append(data)

            statement = statement.select(Cars).options(*[f'Cars.{x}' for x in column_list])
        """filter in fastapi query looks like: key*value-key*value-..."""
        if filter_by is not None and filter_by != 'null':
            criteria = dict(x.split('*') for x in filter_by.split('-'))

            criteria_list = []
            for attr,value in criteria.items():
                _attr = getattr(Cars, attr)
                search = "%{}%".format(value)
                criteria_list.append(_attr.like(search))

            statement = statement.filter(or_(*criteria_list))



        """sort in fastapi query looks like make-model-vin..."""
        if sort is not None and sort != 'null':
            split_sort = sort.split('-')
            new_sort = ','.join(split_sort)
            statement = statement.order_by(desc(text(new_sort)))


        """pagination"""
        offset_page = page - 1
        statement = statement.offset(offset_page * limit).limit(limit)
        """count query"""
        count_query = select(func.count(1)).select_from(Cars)
        """Total record"""
        total_record = (await session.exec(count_query)).one() or 0
        """total page"""
        total_page = math.ceil(total_record / limit)

        res = await session.exec(statement)
        result = res.unique().all()
        return PageResponse(
            page_number=page,
            page_size=limit,
            total_pages=total_page,
            total_records=total_record,
            content=result
        )



    async def create_car(self, car_data: CarCreateSchema, session: AsyncSession):
        new_expenses = []
        if car_data.expenses:
            new_expenses = [Expenses(**exp.model_dump()) for exp in car_data.expenses]
        new_car = Cars(**car_data.model_dump(exclude={"expenses"}), expenses=new_expenses)
        session.add(new_car)
        await session.commit()
        await session.refresh(new_car)
        return new_car




    async def update_car(self, car_uid: str, update_data: CarUpdateSchema, session: AsyncSession):
        car_to_update = await self.get_car(car_uid, session)
        if car_to_update:
            update_data_dict = update_data.model_dump()
            for k,v in update_data_dict.items():
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

    async def create_expense(self, car_uid: str, exp_data: ExpensesCreateSchema, session: AsyncSession):
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
