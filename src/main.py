from fastapi import FastAPI
from src.cars.routes import car_router
from src.auth.routes import auth_router


version = 'v1'

app = FastAPI(
    title = 'My_Whip',
    description = 'A REST API for a Car-CRM web service',
    version = version
)

app.include_router(car_router, prefix=f'/api/{version}/cars', tags=['cars'])
#.include_router(auth_router, prefix=f'/api/{version}/auth', tags=['auth'])
