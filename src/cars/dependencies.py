from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends

from ..db.core import get_session
from .service import CarService, ExpensesService
from .repositories import CarsRepository, ExpensesRepository
from ..directories.dependencies import get_dir_service
from ..directories.service import DirectoryService


def get_car_repository(session: AsyncSession = Depends(get_session)) -> CarsRepository:
    return CarsRepository(session)


def get_car_service(
    repository: CarsRepository = Depends(get_car_repository),
    dir_service: DirectoryService = Depends(get_dir_service),
) -> CarService:
    return CarService(repository, dir_service)


def get_exp_repository(
    session: AsyncSession = Depends(get_session),
) -> ExpensesRepository:
    return ExpensesRepository(session)


def get_exp_service(
    repository: ExpensesRepository = Depends(get_exp_repository),
    car_service: CarService = Depends(
        get_car_service
    ),  # to have access to it's methods
) -> ExpensesService:
    return ExpensesService(repository, car_service)
