from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends

from ..db.main import get_session
from .service import CarService, ExpensesService


def get_car_service(session: AsyncSession = Depends(get_session)) -> CarService:
    return CarService(session)


def get_exp_service(session: AsyncSession = Depends(get_session)) -> ExpensesService:
    return ExpensesService(session)
