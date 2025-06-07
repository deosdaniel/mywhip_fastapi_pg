from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends

from ..db.core import get_session
from .service import CarService, ExpensesService
from .repositories import CarsRepository


def get_car_repository(session: AsyncSession = Depends(get_session)) -> CarsRepository:
    return CarsRepository(session)


def get_car_service(
    repository: CarsRepository = Depends(get_car_repository),
) -> CarService:
    return CarService(repository)


def get_exp_service(session: AsyncSession = Depends(get_session)) -> ExpensesService:
    return ExpensesService(session)
