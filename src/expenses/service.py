from sqlmodel.ext.asyncio.session import AsyncSession

from .schemas import ExpensesSchema, ExpensesCreateSchema
from sqlmodel import select, desc
from .models import Expenses


class ExpensesService:

    async def create_expense(self, car_uid: str, exp_data: ExpensesCreateSchema, session: AsyncSession):
        exp_data_dict = exp_data.model_dump()
        new_exp = ExpensesCreateSchema(**exp_data_dict)
        #new_exp.car_uid = car_uid

        session.add(new_exp)
        await session.commit()
        return new_exp

    async def get_expenses(self, car_uid: str, session: AsyncSession):
        statement = select(Expenses).where(Expenses.car_uid == car_uid)
        result = await session.exec(statement)
        exps = result.all()
        if exps is not None:
            return exps
        else:
            return None