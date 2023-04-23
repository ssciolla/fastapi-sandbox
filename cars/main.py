from enum import Enum
# from typing import Annotated

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class FuelType(Enum):
    electric = 'electric'
    gas = 'gas'
    hybrid = 'hybrid'
    plug_in_hybrid = 'plug-in hybrid'


class Brand(BaseModel):
    name: str
    founded: int


class EntityWithID(BaseModel):
    id: int


class Car(BaseModel):
    brand: Brand
    model: str
    fuel_type: FuelType


class CarWithID(Car, EntityWithID):
    pass


CARS: list[CarWithID] = []


app = FastAPI()


# Routes
@app.post("/cars/")
async def create_car(car: Car) -> CarWithID:
    if len(CARS) > 0:
        next_id = (max([car.id for car in CARS]) + 1)
    else:
        next_id = 0
    car_with_id = CarWithID(
        id=next_id,
        brand=car.brand,
        model=car.model,
        fuel_type=car.fuel_type
    )
    CARS.append(car_with_id)
    return car_with_id


@app.get("/cars/")
async def get_cars() -> list[CarWithID]:
    return CARS


@app.delete("/cars/")
async def delete_car(car_id: int):
    new_cars = [car for car in CARS if car.id != car_id]
    if len(new_cars) < len(CARS):
        CARS = new_cars
        return
    raise HTTPException(404, 'no car with that ID')
