from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from src.cars.routes import car_router, expenses_router, directory_router
from src.auth.routes import auth_router


from fastapi.responses import JSONResponse
from fastapi.requests import Request
from src.utils.exceptions import VinBusyException, EntityNotFoundException

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


@app.exception_handler(VinBusyException)
def vin_exception_handler(request: Request, exc: VinBusyException):
    return JSONResponse(
        content={
            "status": "Failed",
            "message": f"Sorry, a vehicle with this VIN-number is currently possessed by someone else.",
        },
    )


@app.exception_handler(EntityNotFoundException)
def entity_not_found(request: Request, exc: EntityNotFoundException):
    return JSONResponse(
        content={
            "status": "Failed",
            "message": f"Sorry, requested {exc.entity} does not exist.",
        }
    )


app.include_router(car_router, prefix=f"/api/{version}/cars", tags=["Cars"])
app.include_router(expenses_router, prefix=f"/api/{version}/cars", tags=["Expenses"])
app.include_router(
    directory_router, prefix=f"/api/{version}/directories", tags=["Directories"]
)
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Auth"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
