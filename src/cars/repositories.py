from sqlalchemy import func, desc, asc
from sqlmodel import select, update
from src.cars.models import Cars, Expenses
from src.cars.schemas import GetAllFilter
from src.utils.base_service_repo import BaseRepository


class CarsRepository(BaseRepository):
    async def check_vin_collision(self, vin: str) -> bool:
        statement = select(Cars).where(Cars.vin == vin).where(Cars.status != "SOLD")
        check_vin = await self.session.exec(statement)
        return check_vin.one_or_none() is not None

    async def create_car(self, new_car_dict: dict) -> Cars:
        car = Cars(**new_car_dict)
        self.session.add(car)
        await self.session.commit()
        return car

    async def get_car_by_uid(self, car_uid: str) -> Cars:
        car = await self.session.exec(select(Cars).where(Cars.uid == car_uid))
        return car.one_or_none()

    async def get_cars_filtered(self, offset_page, filter_schema: GetAllFilter):
        # Base query
        statement = select(Cars)
        # Filtering
        if filter_schema.make:
            statement = statement.filter_by(make=filter_schema.make)
        if filter_schema.model:
            statement = statement.filter_by(model=filter_schema.model)
        if filter_schema.prod_year:
            if filter_schema.prod_year.year_from:
                statement = statement.filter(
                    Cars.year >= filter_schema.prod_year.year_from
                )
            if filter_schema.prod_year.year_to:
                statement = statement.filter(
                    Cars.year <= filter_schema.prod_year.year_to
                )
        if filter_schema.status:
            statement = statement.filter_by(status=filter_schema.status)
        # Sorting
        direction = desc if filter_schema.order_desc else asc
        if filter_schema.sort_by:
            statement = statement.order_by(
                direction(getattr(Cars, filter_schema.sort_by))
            )

        statement = statement.offset(offset_page * filter_schema.limit).limit(
            filter_schema.limit
        )
        cars = await self.session.exec(statement)
        return cars

    async def count_filtered_records(self, filter_schema: GetAllFilter) -> int:
        statement = select(func.count(Cars.uid))
        if filter_schema.make:
            statement = statement.filter_by(make=filter_schema.make)
        if filter_schema.model:
            statement = statement.filter_by(model=filter_schema.model)
        if filter_schema.prod_year:
            if filter_schema.prod_year.year_from:
                statement = statement.filter(
                    Cars.year >= filter_schema.prod_year.year_from
                )
                if filter_schema.prod_year.year_to:
                    statement = statement.filter(
                        Cars.year <= filter_schema.prod_year.year_to
                    )
        if filter_schema.status:
            statement = statement.filter_by(status=filter_schema.status)

        result = await self.session.exec(statement)
        return result.one()

    async def update_car(self, car_uid: str, car_update_dict: dict) -> Cars:
        car = await self.get_car_by_uid(car_uid)
        if not car:
            return None
        await self.session.exec(
            update(Cars).where(Cars.uid == car_uid).values(**car_update_dict)
        )
        await self.session.commit()
        await self.session.refresh(car)
        return car

    async def delete_car(self, car_uid: str) -> bool:
        car_to_delete = await self.get_car_by_uid(car_uid)
        if not car_to_delete:
            return False
        await self.session.delete(car_to_delete)
        await self.session.commit()
        return True


class ExpensesRepository(BaseRepository):
    async def create_expense(self, car_uid: str, exp_data_dict: dict) -> Expenses:
        new_exp = Expenses(**exp_data_dict)
        new_exp.car_uid = car_uid
        self.session.add(new_exp)
        await self.session.commit()
        return new_exp

    async def get_single_exp(self, car_uid: str, expense_uid: str) -> Expenses:
        pass

    async def count_exp_by_car_uid(self, car_uid: str) -> int:
        pass

    async def get_exp_by_car_uid(self, car_uid: str) -> Expenses:
        pass

    async def update_single_exp(self, car_uid: str, expense_uid: str) -> Expenses:
        pass

    async def delete_single_exp(self, car_uid: str, expense_uid: str) -> bool:
        pass

    async def delete_exp_by_car_uid(self, car_uid: str) -> bool:
        pass
