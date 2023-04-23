from enum import Enum
from typing import Annotated

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel


class PokemonName(str, Enum):
    charmander = 'Charmander'
    squirtle = 'Squirtle'
    bulbasaur = 'Bulbasaur'


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


# Data
fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"}
]


# Hello world
@app.get("/")
async def root():
    return {"message": "Hello World"}


# Path parameter example
@app.get("/items/{item_id}")
async def read_item(
    item_id: Annotated[int, Path(title='The ID of the item to get', le=5)],
    q: str | None = None,
    short: bool = False
):
    item: dict[str, str | int] = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "this item is special"})
    return item


# Enum example
@app.get("/pokemon/{pokemon_name}/")
async def get_pokemon(pokemon_name: PokemonName):
    match pokemon_name:
        case PokemonName.squirtle:
            type = "water"
        case PokemonName.charmander:
            type = "fire"
        case PokemonName.bulbasaur:
            type = "grass"
    return {"name": pokemon_name, "type": type}


# Path example
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


# Query Parameters
# @app.get("/items/")
# async def read_items(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip:(skip + limit)]


# Body example with Pydantic model
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# Extra validation example
@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(min_length=3, max_length=50)] = None):
    results: dict[str, list[dict[str, str]] | str] = {"items": fake_items_db}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/repeated-query/")
async def read_items_repeated_query(q: Annotated[list[str] | None, Query()] = None):
    return {"q": q}

