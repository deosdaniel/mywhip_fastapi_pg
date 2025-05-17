from fastapi import FastAPI
from src.cars.routes import car_router
from contextlib import asynccontextmanager
from src.db.main import init_db


@asynccontextmanager
async def life_span(app: FastAPI):
    print('Server starting ... ')
    await init_db()
    yield
    print('Server has been stopped.')

version = 'v1'

app = FastAPI(
    title = 'My_Whip',
    description = 'A REST API for a Car-CRM web service',
    version = version,
    lifespan = life_span
)

app.include_router(car_router, prefix=f'/api/{version}/cars', tags=['cars'])