from fastapi import FastAPI
from src.cars.routes import car_router
from src.expenses.routes import expense_router
from src.auth.routes import auth_router
from src.db.main import init_db


version = 'v1'

app = FastAPI(
    title = 'My_Whip',
    description = 'A REST API for a Car-CRM web service',
    version = version
)

app.include_router(car_router, prefix=f'/api/{version}/cars', tags=['cars'])
app.include_router(auth_router, prefix=f'/api/{version}/auth', tags=['auth'])
app.include_router(expense_router, prefix=f'/api/{version}/expenses', tags=['expenses'])
