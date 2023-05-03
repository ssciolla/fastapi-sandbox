import os
from enum import Enum

from typing import Optional
from sqlmodel import create_engine, Field, Relationship, SQLModel


# Brand

class BrandBase(SQLModel):
    name: str = Field(index=True)


class Brand(BrandBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cars: list['Car'] = Relationship(back_populates='brand')


class BrandCreate(BrandBase):
    pass


class BrandRead(BrandBase):
    id: int


# Car

class FuelType(Enum):
    electric = 'electric'
    gas = 'gas'
    hybrid = 'hybrid'
    plug_in_hybrid = 'plug-in hybrid'


class CarBase(SQLModel):
    model: str
    fuel_type: FuelType
    brand_id: Optional[int] = Field(default=None, foreign_key='brand.id')


class Car(CarBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    brand: Optional[Brand] = Relationship(back_populates='cars')


class CarCreate(CarBase):
    brand_id: int


class CarRead(CarBase):
    id: int
    brand_id: int


# Multiple models

class CarReadWithBrand(CarRead):
    brand: Optional[BrandRead] = None


class BrandReadWithCars(BrandRead):
    cars: list[CarRead] = []


# DB setup


sqlite_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cars.db')
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {'check_same_thread': False}
ENGINE = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def set_up_database():
    SQLModel.metadata.create_all(ENGINE)


if __name__ == '__main__':
    set_up_database()
