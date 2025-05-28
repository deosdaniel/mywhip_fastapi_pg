from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.cars.models import Cars
from src.cars.routes import car_router
from src.auth.routes import auth_router
from src.db.main import engine, SQLModel, get_session
from src.db.demo_data import generate_demo_cars

version = "v1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код, выполняемый при запуске приложения
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("Tables created")

    #    # Заполнение тестовыми данными (если таблица пуста)
    #    async with AsyncSession(engine) as session:
    #        existing_cars = await session.exec(select(Cars))
    #        if not existing_cars.first():
    #            demo_cars = generate_demo_cars(100)
    #            session.add_all(demo_cars)
    #            await session.commit()
    #            print("Demo data added")
    #
    yield  # Здесь приложение работает

    # Код, выполняемый при остановке приложения


#    async with engine.begin() as conn:
#        await conn.run_sync(SQLModel.metadata.drop_all)
#    print("Tables dropped")


app = FastAPI(
    title="My_Whip",
    description="A REST API for a Car-CRM web service",
    version=version,
    lifespan=lifespan,
)

app.include_router(car_router, prefix=f"/api/{version}/cars", tags=["cars"])
# app.include_router(auth_router, prefix=f'/api/{version}/auth', tags=['auth'])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
