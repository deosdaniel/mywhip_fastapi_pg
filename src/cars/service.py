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
    UserShortSchema,
    ExpensesUpdateSchema,
)
from src.utils.exceptions import VinBusyException, EntityNotFoundException

from src.directories.service import DirectoryService
from ..users.schemas import UserSchema, UserRole
from ..utils.base_service_repo import BaseService
from ..utils.normalize_make_model import normalize_make_model


def calculate_car_metrics(car: CarSchema) -> dict:
    total_expenses = sum(
        (exp.exp_summ for exp in car.expenses if exp.type != "PURCHASE") or []
    )
    price_purchased = sum(
        (exp.exp_summ for exp in car.expenses if exp.type == "PURCHASE") or []
    )
    total_cost = total_expenses + price_purchased
    potential_profit = (car.price_listed - total_cost) if car.price_listed else 0
    potential_margin = (
        round(potential_profit / total_cost * 100, 2) if total_cost else 0
    )

    profit = (car.price_sold - total_cost) if car.price_sold else 0
    margin = round(profit / total_cost * 100, 2) if total_cost else 0

    return {
        "price_purchased": price_purchased,
        "total_expenses": total_expenses,
        "total_cost": total_cost,
        "profit": profit,
        "margin": margin,
        "potential_profit": potential_profit,
        "potential_margin": potential_margin,
    }


def get_expenses_by_owner(car: CarSchema) -> dict[UUID, int]:
    expenses_by_user = defaultdict(int)

    for exp in car.expenses or []:
        if exp.user and exp.user.uid:
            expenses_by_user[exp.user.uid] += exp.exp_summ

    return expenses_by_user


def build_owners_stats(
    car: CarSchema, expenses_by_user: dict[UUID, int], profit: int
) -> list[OwnerStats]:
    owners = [car.primary_owner_uid] + [owner.uid for owner in car.secondary_owners]
    owners_count = len(owners)
    profit_per_owner = profit / owners_count if owners_count else 0

    # Сопоставляем UID → UserShortSchema из расходов
    users_map = {
        exp.user.uid: exp.user
        for exp in car.expenses or []
        if exp.user and exp.user.uid
    }

    # Добавим primary_owner, если его нет
    if car.primary_owner_uid not in users_map:
        po = getattr(car, "primary_owner", None)
        users_map[car.primary_owner_uid] = UserShortSchema(
            uid=car.primary_owner_uid,
            email=getattr(po, "email", "unknown@email.com"),
            username=getattr(po, "username", "Unknown"),
        )

    # Добавим secondary_owners, если их нет
    for owner in car.secondary_owners:
        if owner.uid not in users_map:
            users_map[owner.uid] = UserShortSchema(
                uid=owner.uid,
                email=owner.email or "unknown@email.com",
                username=owner.username or "Unknown",
            )

    return [
        OwnerStats(
            owner_uid=uid,
            username=users_map[uid].username,
            email=users_map[uid].email,
            owner_total_expenses=expenses_by_user.get(uid, 0),
            net_payout=expenses_by_user.get(uid, 0) + profit_per_owner,
        )
        for uid in owners
    ]


def calculate_stats(car: CarSchema) -> CarStats:
    metrics = calculate_car_metrics(car)
    expenses_by_user = get_expenses_by_owner(car)
    owners_stats = build_owners_stats(car, expenses_by_user, metrics["profit"])

    return CarStats(
        price_purchased=metrics["price_purchased"],
        total_expenses=metrics["total_expenses"],
        total_cost=metrics["total_cost"],
        potential_profit=metrics["potential_profit"],
        potential_margin=metrics["potential_margin"],
        profit=metrics["profit"],
        margin=metrics["margin"],
        owners_count=len(expenses_by_user),
        profit_per_owner=(
            metrics["profit"] / len(expenses_by_user) if expenses_by_user else 0
        ),
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
                selectinload(Cars.primary_owner),
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
        exp_update_data: ExpensesUpdateSchema,
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
