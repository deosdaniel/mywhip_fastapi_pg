from sqlalchemy import delete
from sqlalchemy.orm import joinedload, selectinload
from sqlmodel.ext.asyncio.session import AsyncSession

from .schemas import CarCreateSchema, CarUpdateSchema, ExpensesSchema, ExpensesCreateSchema
from sqlmodel import select, desc
from .models import Cars, Expenses
from datetime import datetime


"""Cars"""

class CarService:
    async def get_car(self, car_uid: str, session: AsyncSession):
        statement = select(Cars).options(selectinload(Cars.expenses)).where(Cars.uid == car_uid)
        res = await session.exec(statement)
        car = res.first()
        print(f'This is your car :{car}')
        if car is not None:
            return car
        else:
            return None

    async def get_all_cars(self, session: AsyncSession):
        statement  = select(Cars).options(selectinload(Cars.expenses))      # selectinload нужен для корректной подгрузки вложенных сущностей
        res = await session.exec(statement)
        result = res.unique().all()                                         # unique избавляет от повторяющихся строчек при джойне
        return result



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
