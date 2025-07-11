from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import func, desc, asc, and_, or_
from sqlalchemy.orm import selectinload
from sqlmodel import select, update
from src.cars.models import Cars, Expenses
from src.cars.schemas import GetAllFilter
from src.shared.car_user_link import CarUserLink
from src.utils.base_service_repo import BaseRepository


class CarsRepository(BaseRepository):

    async def check_vin_collision(self, vin: str) -> Cars:
        statement = select(Cars).where(Cars.vin == vin, Cars.status != "SOLD")
        result = await self.session.exec(statement)
        return result.one_or_none()

    async def add_owner_to_car(self, car_uid: UUID, user_uid: UUID):
        link = CarUserLink(car_uid=car_uid, user_uid=user_uid)
        self.session.add(link)
        await self.session.commit()
        self.session.expire_all()

    async def delete_owner_from_car(self, car_uid: UUID, user_uid: UUID):
        statement = select(CarUserLink).where(
            and_(CarUserLink.car_uid == car_uid, CarUserLink.user_uid == user_uid)
        )
        result = await self.session.exec(statement)
        link = result.one_or_none()
        if link:
            await self.session.delete(link)
            await self.session.commit()
            return True
        else:
            return False

    async def get_my_cars(
        self,
        offset_page: int,
        limit: int,
        owner_uid: UUID,
        sort_by: Optional[str] = None,
        order: str = "desc",
    ):
        statement = (
            select(Cars)
            .outerjoin(CarUserLink, Cars.uid == CarUserLink.car_uid)
            .where(
                or_(
                    Cars.primary_owner_uid == owner_uid,
                    CarUserLink.user_uid == owner_uid,
                )
            )
            .offset(offset_page)
            .limit(limit)
        )
        if sort_by:
            sort_column = getattr(Cars, sort_by, None)
            if sort_column is None:
                raise HTTPException(
                    status_code=422, detail=f"Invalid sort field: {sort_by}"
                )
            if order == "desc":
                statement = statement.order_by(desc(sort_column))
            else:
                statement = statement.order_by(asc(sort_column))

        return await self.session.exec(statement)

    async def count_my_cars(self, owner_uid: UUID):
        result = await self.session.exec(
            select(func.count(Cars.uid)).where(Cars.primary_owner_uid == owner_uid)
        )
        return result.one()

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
        direction = desc if (filter_schema.order_desc == "desc") else asc
        if filter_schema.sort_by:
            statement = statement.order_by(
                direction(getattr(Cars, filter_schema.sort_by))
            )

        statement = statement.offset(offset_page).limit(filter_schema.limit)
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


class ExpensesRepository(BaseRepository):
    async def create_expense(self, car_uid: UUID, exp_data_dict: dict) -> Expenses:

        new_exp = Expenses(**exp_data_dict)
        new_exp.car_uid = car_uid
        self.session.add(new_exp)
        await self.session.commit()
        await self.session.refresh(new_exp, attribute_names=["user"])
        return new_exp

    async def get_single_exp(self, car_uid: UUID, expense_uid: str) -> Expenses:
        statement = (
            select(Expenses)
            .options(selectinload(Expenses.user))
            .where(Expenses.car_uid == car_uid)
            .where(Expenses.uid == expense_uid)
        )
        result = await self.session.exec(statement)
        return result.one_or_none()

    async def get_exp_by_car_uid(
        self,
        car_uid: UUID,
        offset_page: int,
        limit: int,
        sort_by: Optional[str] = None,
        order: str = "desc",
    ) -> list[Expenses]:
        statement = (
            select(Expenses)
            .options(selectinload(Expenses.user))
            .where(Expenses.car_uid == car_uid)
            .offset(offset_page)
            .limit(limit)
        )
        if sort_by:
            sort_column = getattr(Expenses, sort_by, None)
            if sort_column is None:
                raise HTTPException(
                    status_code=422, detail=f"Invalid sort field: {sort_by}"
                )
            if order == "desc":
                statement = statement.order_by(desc(sort_column))
            else:
                statement = statement.order_by(asc(sort_column))
        return await self.session.exec(statement)

    async def count_exp_by_car_uid(self, car_uid: UUID) -> int:
        count_statement = (
            select(func.count(1))
            .select_from(Expenses)
            .where(Expenses.car_uid == car_uid)
        )
        result = await self.session.exec(count_statement)
        return result.one()

    async def update_single_exp(
        self, car_uid: UUID, expense_uid: UUID, update_data_dict: dict
    ) -> Expenses:
        exp = await self.get_single_exp(car_uid, expense_uid)
        await self.session.exec(
            update(Expenses)
            .where(Expenses.car_uid == car_uid)
            .where(Expenses.uid == expense_uid)
            .values(**update_data_dict)
        )
        await self.session.commit()
        await self.session.refresh(exp)
        return exp

    async def delete_single_exp(self, car_uid: UUID, expense_uid: UUID) -> bool:
        exp_to_delete = await self.get_single_exp(car_uid, expense_uid)
        if exp_to_delete:
            await self.session.delete(exp_to_delete)
            await self.session.commit()
            return True
        else:
            return False

    async def delete_exp_by_car_uid(self, car_uid: UUID) -> bool:
        result = await self.session.exec(
            select(Expenses).where(Expenses.car_uid == car_uid)
        )
        exps = result.all()
        for exp in exps:
            await self.session.delete(exp)
        await self.session.commit()
        return True
