import math
from collections import defaultdict
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload

from src.utils.schemas_common import PageResponse
from .models import Cars, Expenses
from .repositories import CarsRepository, ExpensesRepository
from .schemas import (
    CarCreateSchema,
    CarUpdateSchema,
    ExpensesCreateSchema,
    GetAllFilter,
    CarSchema,
    CarStats,
    CarCreateResponse,
    OwnerStats,
)
from src.utils.exceptions import VinBusyException, EntityNotFoundException

from src.directories.service import DirectoryService
from ..users.schemas import UserSchema, UserRole
from ..utils.base_service_repo import BaseService
from ..utils.normalize_make_model import normalize_make_model


def calculate_stats(car: CarSchema) -> CarStats:
    owners_count = 1 + len(car.secondary_owners)

    # Общие расходы на автомобиль (включая цену покупки)
    total_expenses = sum(exp.exp_summ for exp in car.expenses or [])
    total_cost = car.price_purchased + total_expenses

    # Потенциальная прибыль и маржа (если ещё не продано)
    potential_profit = (car.price_listed - total_cost) if car.price_listed else 0
    potential_margin = (
        round(potential_profit / total_cost * 100, 2) if total_cost else 0
    )

    # Фактическая прибыль и маржа (если продано)
    profit = (car.price_sold - total_cost) if car.price_sold else 0
    margin = round(profit / total_cost * 100, 2) if total_cost else 0
    profit_per_owner = (profit / owners_count) if owners_count else profit

    # Расчёт индивидуальных выплат
    expenses_by_user: dict[UUID, int] = defaultdict(int)
    for exp in car.expenses or []:
        if exp.user_uid:
            expenses_by_user[exp.user_uid] += exp.exp_summ

    # Добавляем расходы на покупку к создателю карточки
    if car.primary_owner_uid:
        expenses_by_user[car.primary_owner_uid] += car.price_purchased or 0

    owner_infos = {}

    if car.primary_owner_uid:
        owner_infos[car.primary_owner_uid] = {
            "uid": car.primary_owner_uid,
            "username": (
                getattr(car, "primary_owner", None).username
                if hasattr(car, "primary_owner")
                else "—"
            ),
            "email": (
                getattr(car, "primary_owner", None).email
                if hasattr(car, "primary_owner")
                else "—"
            ),
        }

    for owner in car.secondary_owners or []:
        owner_infos[owner.uid] = {
            "uid": owner.uid,
            "username": owner.username,
            "email": owner.email,
        }

    # Формируем итоговую статистику по каждому владельцу
    owners_stats = []

    for uid, personal_expenses in expenses_by_user.items():
        info = owner_infos.get(uid)
        if info:
            owners_stats.append(
                OwnerStats(
                    owner_uid=uid,
                    username=info["username"],
                    email=info["email"],
                    total_expenses=personal_expenses,
                    net_payout=round(personal_expenses + profit_per_owner, 2),
                )
            )

    return CarStats(
        total_expenses=total_expenses,
        total_cost=total_cost,
        potential_profit=potential_profit,
        potential_margin=potential_margin,
        profit=profit,
        margin=margin,
        owners_count=owners_count,
        profit_per_owner=round(profit_per_owner, 2),
        owners_stats=owners_stats,
    )


# Cars
class CarService(BaseService[CarsRepository]):
    # Add car_service to have access to it's methods
    def __init__(self, repository: CarsRepository, dir_service: DirectoryService):
        super().__init__(repository)
        self.dir_service = dir_service

    # Create a Car
    async def create_car(
        self,
        car_data: CarCreateSchema,
        primary_owner_uid: UUID,
    ):
        vin_collision = await self.repository.check_vin_collision(car_data.vin)
        if vin_collision:
            raise VinBusyException
        await self.dir_service.validate_make_model(car_data.make, car_data.model)

        new_car_dict = car_data.model_dump()
        new_car_dict["make"] = normalize_make_model(car_data.make)
        new_car_dict["model"] = normalize_make_model(car_data.model)
        new_car_dict["primary_owner_uid"] = primary_owner_uid
        car = await self.repository.create(table=Cars, new_entity_dict=new_car_dict)
        return car

    async def get_my_cars(
        self,
        page: int,
        limit: int,
        owner_uid: UUID,
        sort_by: str = "created_at",
        allowed_sort_fields: Optional[list[str]] = None,
        order: str = "desc",
    ):
        offset_page = (page - 1) * limit

        if allowed_sort_fields and sort_by not in allowed_sort_fields:
            raise HTTPException(
                status_code=400, detail=f"Sorting by '{sort_by}' is not allowed."
            )
        cars = await self.repository.get_my_cars(
            offset_page=offset_page,
            limit=limit,
            sort_by=sort_by,
            order=order,
            owner_uid=owner_uid,
        )

        total_records = await self.repository.count_my_cars(owner_uid)
        total_pages = math.ceil(total_records / limit)
        return PageResponse(
            page_number=page,
            page_size=limit,
            total_pages=total_pages,
            total_records=total_records,
            content=cars,
        )

    async def get_car_all_owners(self, car_uid: str, current_user: UserSchema):
        car = await self.get_by_uid(
            Cars,
            car_uid,
            options=[
                selectinload(Cars.expenses).joinedload(Expenses.user),
                selectinload(Cars.secondary_owners),
            ],
        )
        if not car:
            raise EntityNotFoundException("car_uid")
        if current_user.role != UserRole.ADMIN:
            is_primary = car.primary_owner_uid == current_user.uid
            is_secondary = any(
                owner.uid == current_user.uid for owner in car.secondary_owners
            )
            if not (is_primary or is_secondary):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
                )
        stats = calculate_stats(car)
        return CarSchema.model_validate(car, from_attributes=True).model_copy(
            update={"stats": stats}
        )

    async def get_car_with_primary_owner_check(
        self, car_uid: str, current_user: UserSchema
    ):
        car = await self.get_by_uid(
            table=Cars,
            uid=car_uid,
            options=[
                selectinload(Cars.secondary_owners),
                selectinload(Cars.expenses).joinedload(Expenses.user),
            ],
        )

        if not car:
            raise EntityNotFoundException("car_uid")
        if current_user.role != UserRole.ADMIN and str(car.primary_owner_uid) != str(
            current_user.uid
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )
        return car

    async def add_owner(
        self, car_uid: str, new_owner_uid: str, current_user: UserSchema
    ):
        await self.get_car_with_primary_owner_check(car_uid, current_user)
        await self.repository.add_owner_to_car(car_uid, new_owner_uid)
        car = await self.repository.get_by_uid(
            table=Cars, uid=car_uid, options=[selectinload(Cars.secondary_owners)]
        )
        return car

    async def delete_owner(
        self, car_uid: str, delete_owner_uid: str, current_user: UserSchema
    ):
        car = await self.get_car_with_primary_owner_check(car_uid, current_user)
        delete_owner_uuid = UUID(delete_owner_uid)
        if car.primary_owner_uid == delete_owner_uuid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Primary owner cannot remove themselves from ownership",
            )
        else:
            delete_owner = await self.repository.delete_owner_from_car(
                car_uid, delete_owner_uid
            )
            if delete_owner:
                return True
            else:
                raise EntityNotFoundException("owner")

    async def update_car(
        self, car_uid: UUID, car_data: CarUpdateSchema, current_user: UserSchema
    ) -> Cars:
        await self.get_car_all_owners(car_uid=car_uid, current_user=current_user)
        return await self.update_by_uid(Cars, car_uid, car_data)

    async def delete_car(self, car_uid: UUID, current_user: UserSchema) -> None:
        await self.get_car_with_primary_owner_check(car_uid, current_user)
        return await self.delete_by_uid(Cars, car_uid)

    # Get Cars filtered list
    async def filter_all_cars(
        self,
        filter_schema: GetAllFilter,
    ):

        offset_page = (filter_schema.page - 1) * filter_schema.limit

        cars = await self.repository.get_cars_filtered(offset_page, filter_schema)

        total_records = await self.repository.count_filtered_records(filter_schema)
        total_pages = math.ceil(total_records / filter_schema.limit)
        return PageResponse(
            page_number=filter_schema.page,
            page_size=filter_schema.limit,
            total_pages=total_pages,
            total_records=total_records,
            content=cars,
        )


# Expenses
class ExpensesService(BaseService[ExpensesRepository]):
    # Add car_service to have access to it's methods
    def __init__(self, repository: ExpensesRepository, car_service: CarService):
        super().__init__(repository)
        self.car_service = car_service

    # Create an expense
    async def create_expense(
        self, car_uid: UUID, exp_data: ExpensesCreateSchema, current_user: UserSchema
    ) -> Expenses:
        await self.car_service.get_car_all_owners(
            car_uid=car_uid, current_user=current_user
        )
        exp_data_dict = exp_data.model_dump()
        exp_data_dict["user_uid"] = current_user.uid
        new_exp = await self.repository.create_expense(car_uid, exp_data_dict)
        return new_exp

    # Get single expense
    async def get_single_expense(
        self, car_uid: UUID, exp_uid: str, current_user: UserSchema
    ) -> Expenses:
        await self.car_service.get_car_all_owners(
            car_uid=car_uid, current_user=current_user
        )
        exp = await self.repository.get_single_exp(car_uid, exp_uid)
        if not exp:
            raise EntityNotFoundException("exp_uid")
        return exp

    # Update single expense
    async def update_single_expense(
        self,
        car_uid: UUID,
        exp_uid: UUID,
        exp_update_data: ExpensesCreateSchema,
        current_user: UserSchema,
    ) -> Expenses:
        exp = await self.get_single_expense(car_uid, exp_uid, current_user)
        if (exp.user.uid != current_user.uid) and (current_user.role != UserRole.ADMIN):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )
        update_data_dict = exp_update_data.model_dump(exclude_unset=True)
        updated_exp = await self.repository.update_single_exp(
            car_uid, exp_uid, update_data_dict
        )
        return updated_exp

    # Delete single expense
    async def delete_single_expense(
        self,
        car_uid: UUID,
        exp_uid: UUID,
        current_user: UserSchema,
    ):
        exp = await self.get_single_expense(car_uid, exp_uid, current_user)
        if (exp.user.uid != current_user.uid) and (current_user.role != UserRole.ADMIN):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )
        delete_exp = await self.repository.delete_single_exp(car_uid, exp_uid)
        if delete_exp:
            return True
        else:
            raise EntityNotFoundException("exp_uid")

    # Get all expenses for a single car
    async def get_expenses_by_car_uid(
        self,
        car_uid: UUID,
        current_user: UserSchema,
        page: int = 1,
        limit: int = 10,
        sort_by: str = "created_at",
        allowed_sort_fields: Optional[list[str]] = None,
        order: str = "desc",
    ) -> list[Expenses]:
        await self.car_service.get_car_all_owners(
            car_uid=car_uid, current_user=current_user
        )

        offset_page = (page - 1) * limit

        if allowed_sort_fields and sort_by not in allowed_sort_fields:
            raise HTTPException(
                status_code=400, detail=f"Sorting by '{sort_by}' is not allowed."
            )
        expenses = await self.repository.get_exp_by_car_uid(
            car_uid=car_uid,
            offset_page=offset_page,
            limit=limit,
            sort_by=sort_by,
            order=order,
        )

        total_records = await self.repository.count_exp_by_car_uid(car_uid)
        total_pages = math.ceil(total_records / limit)

        return PageResponse(
            page_number=page,
            page_size=limit,
            total_pages=total_pages,
            total_records=total_records,
            content=expenses,
        )

    # Delete all expenses for a single car
    async def delete_all_expenses_by_car_uid(
        self, car_uid: UUID, current_user: UserSchema
    ) -> None:
        await self.get_expenses_by_car_uid(car_uid, current_user)
        await self.repository.delete_exp_by_car_uid(car_uid)
        return True
