import logging

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select

from cars.models import (
    Brand, BrandCreate, BrandRead, BrandReadWithCars,
    Car, CarCreate, CarRead, CarReadWithBrand,
    ENGINE, set_up_database
)


logger = logging.getLogger(__name__)

app = FastAPI()


# Dependencies

def get_db_session():
    with Session(ENGINE) as session:
        yield session


# Routes


@app.on_event('startup')
def on_startup():
    set_up_database()


@app.post("/brands/", response_model=BrandRead)
async def create_brand(brand: BrandCreate, session: Session = Depends(get_db_session)):
    db_brand = Brand.from_orm(brand)
    session.add(db_brand)
    session.commit()
    logger.debug(db_brand)
    session.refresh(db_brand)
    return db_brand


@app.get("/brands/", response_model=list[BrandReadWithCars])
async def get_brands(session: Session = Depends(get_db_session)):
    brands = session.exec(select(Brand)).all()
    return brands


@app.delete("/brands/{brand_id}")
async def delete_brand(brand_id: int, session: Session = Depends(get_db_session)):
    statement = select(Brand).where(Brand.id == brand_id)
    results = session.exec(statement)
    brand = results.first()
    logger.debug(brand)
    if brand is None:
        raise HTTPException(404, 'no brand with that ID')
    session.delete(brand)
    session.commit()


@app.post("/cars/", response_model=CarRead)
async def create_car(car: CarCreate, session: Session = Depends(get_db_session)) -> Car:
    db_car = Car.from_orm(car)
    session.add(db_car)
    session.commit()
    logger.debug(db_car)
    session.refresh(db_car)
    return db_car


@app.get("/cars/", response_model=list[CarReadWithBrand])
async def get_cars(session: Session = Depends(get_db_session)):
    cars = session.exec(select(Car)).all()
    return cars


@app.delete("/cars/{car_id}")
async def delete_car(car_id: int, session: Session = Depends(get_db_session)):
    statement = select(Car).where(Car.id == car_id)
    results = session.exec(statement)
    car = results.first()
    logger.debug(car)
    if car is None:
        raise HTTPException(404, 'no car with that ID')
    session.delete(car)
    session.commit()
    return
