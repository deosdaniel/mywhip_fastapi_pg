from sqlmodel.ext.asyncio.session import AsyncSession

from .schemas import CarCreateSchema, CarUpdateSchema
from sqlmodel import select, desc
from .models import Cars
from datetime import datetime

class CarService:
    async def get_car(self, car_uid: str, session: AsyncSession):
        statement = select(Cars).where(Cars.uid == car_uid)
        result = await session.exec(statement)
        car = result.first()
        if car is not None:
            return car
        else:
            return None

    async def get_all_cars(self, session: AsyncSession):
        statement = select(Cars).order_by(desc(Cars.created_at))
        result = await session.exec(statement)
        return result.all()



    async def create_car(self, car_data: CarCreateSchema, session: AsyncSession):
        car_data_dict = car_data.model_dump()                     # превращаем валидированные данные в словарь
        new_car = Cars(                                           # создаем новую машину, присваиваем объект модели Cars
            **car_data_dict)                                      # и распаковываем в этот объект наши данные из словаря

        new_car.date_purchased = datetime.strptime(str(car_data_dict['date_purchased']), '%Y-%m-%d')

        session.add(new_car)
        await session.commit()
        return new_car

    async def update_car(self, car_uid: str, update_data: CarUpdateSchema, session: AsyncSession):
        car_to_update = await self.get_car(car_uid, session)
        if car_to_update:
            update_data_dict = update_data.model_dump()
            for k,v in update_data_dict.items():
                setattr(car_to_update, k, v)

            updated_car = Cars(**update_data_dict)
            updated_car.updated_at = datetime.now()

            await session.commit()
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
