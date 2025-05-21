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

        car_data_dict = car_data.model_dump()                                                                   # превращаем валидированные данные в словарь
        new_car = Cars(                                                                                         # создаем новую машину, присваиваем объект модели Cars
            **car_data_dict)                                                                                    # и распаковываем в этот объект наши данные из словаря

        new_car.date_purchased = datetime.strptime(str(car_data_dict['date_purchased']), '%Y-%m-%d')
        session.add(new_car)
        await session.commit()
        return new_car
        #expenses = car_data.expenses
        #car_data.expenses = []
        #
        #new_car = Expenses(**car_data.model_dump())
        #session.add(new_car)
        #await session.commit()
        #await session.refresh(new_car)
        #new_car.date_purchased = datetime.strptime(str(car_data.model_dump()['date_purchased']), '%Y-%m-%d')
        #for exp in expenses:
        #    new_exp = Expenses(**exp.model_dump())
        #    new_car.car_uid = new_car.uid
        #    session.add(new_exp)
        #    await session.commit()



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
        exp_data_dict = exp_data.model_dump()
        new_exp = Expenses(**exp_data_dict)
        new_exp.car_uid = car_uid

        session.add(new_exp)
        await session.commit()
        return new_exp

    async def get_single_expense(self, exp_uid, session: AsyncSession):
        statement = select(Expenses).where(Expenses.uid == exp_uid)
        result = await session.exec(statement)
        exp = result.first()
        if exp is not None:
            return exp
        else:
            return None

    async def get_expenses(self, car_uid: str, session: AsyncSession):
        statement = select(Expenses).where(Expenses.car_uid == car_uid)
        result = await session.exec(statement)
        exps = result.all()
        if exps is not None:
            return exps
        else:
            return None

    async def delete_expense(self, exp_uid: int, session: AsyncSession):
        exp_to_delete = await self.get_single_expense(exp_uid, session)
        if exp_to_delete is not None:
            await session.delete(exp_to_delete)
            await session.commit()
            return True
        else:
            return None