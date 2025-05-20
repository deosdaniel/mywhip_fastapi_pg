from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.expenses.service import ExpensesService

from src.expenses.schemas import ExpensesSchema, ExpensesCreateSchema

expense_router = APIRouter()

expense_service = ExpensesService()


@expense_router.post('/{car_uid}',status_code=status.HTTP_201_CREATED, response_model=ExpensesSchema)
async def create_expense(
        car_uid: str,
        exp_data: ExpensesCreateSchema,
        session: AsyncSession = Depends(get_session)
) -> dict:

    new_exp = await expense_service.create_expense(car_uid, exp_data, session)

    return new_exp



@expense_router.get('/{car_uid}', response_model=List[ExpensesSchema])
async def get_expenses_single_car(
        car_uid: str,
        session: AsyncSession = Depends(get_session)
):
    result = await expense_service.get_expenses(car_uid,session)
    if result is not None:
        return result
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No expenses yet')

@expense_router.delete('/{exp_uid}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(
        exp_uid: str,
        session: AsyncSession = Depends(get_session)
):
    exp_to_delete = await expense_service.delete_expense(exp_uid,session)

    if exp_to_delete:
        return {}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Exp not found')
