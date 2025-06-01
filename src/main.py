from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from src.cars.routes import car_router, directory_router
from src.cars.routes import expenses_router

version = "v1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="My_Whip",
    description="A REST API for a Car-CRM web service",
    version=version,
    lifespan=lifespan,
)

app.include_router(car_router, prefix=f"/api/{version}/cars", tags=["Cars"])
app.include_router(expenses_router, prefix=f"/api/{version}/cars", tags=["Expenses"])
app.include_router(
    directory_router, prefix=f"/api/{version}/directories", tags=["Directories"]
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
