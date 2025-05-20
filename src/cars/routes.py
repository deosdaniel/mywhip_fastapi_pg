from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from src.cars.schemas import CarSchema, CarUpdateSchema, CarCreateSchema
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session         # Our Dependency
from src.cars.service import CarService     # our CRUD-methods


car_router = APIRouter()

car_service = CarService()



"""Get all cars"""
@car_router.get('/all', response_model=List[CarSchema])
async def get_all_cars(
        session: AsyncSession = Depends(get_session)
):
    books = await car_service.get_all_cars(session)
    return books


"""Get a car by by id"""
@car_router.get('/{car_uid}', response_model=CarSchema)
async def get_car(
        car_uid: str,
        session: AsyncSession = Depends(get_session)
) -> dict:

    car = await car_service.get_car(car_uid, session)

    if car:
        return car
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Car not found')



"""Create new car and add it to table"""
@car_router.post('/', status_code=status.HTTP_201_CREATED, response_model=CarSchema)
async def create_car(
        car_data: CarCreateSchema,
        session: AsyncSession = Depends(get_session)
) -> dict:
    new_car = await car_service.create_car(car_data, session)
    return new_car


"""Update data in a certain car(by id)"""
@car_router.patch('/{car_uid}', response_model=CarSchema)
async def update_car(
        car_uid: str,
        car_update_data: CarUpdateSchema,
        session: AsyncSession = Depends(get_session)
) -> dict:
    updated_car = await car_service.update_car(car_uid, car_update_data, session)

    if not updated_car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cannot update, car does not exist')
    else:
        return updated_car


"""Delete a car by id"""
@car_router.delete('/{car_uid}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_car(
        car_uid: str,
        session: AsyncSession = Depends(get_session)
):

    car_to_delete = await car_service.delete_car(car_uid, session)

    if car_to_delete:
        return {}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cannot delete, car does not exist')

