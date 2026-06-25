
from enum import Enum
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
async def root():
    return "HEllo"

@app.get("/items/{item_id}")
async def read_item(item_id : int):
    return {"item_id": item_id}



fake_db = {
    1 : "Kaustubh",
    2 : "Hema",
    3 : "Sara",
    4 : "John",
    5 : "Dom"

}

@app.get("/users")
async def current_user():
    return {"You are the current user"}

@app.get("/users/{user_id}")
async def get_user_by_id(user_id : int):
    name = fake_db.get(user_id)
    if name is None:
        raise HTTPException(status_code= 404, detail = "UserID not found")
    return {user_id: name}



class Models(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models")
def get_all_models():
    models = []
    for model in Models:
        models.append(model)
    return models

@app.get("/models/{model_name}")
def which_model(model_name : Models):
    return {"model":model_name}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# @app.get("/item")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]


from pydantic import BaseModel


class Item(BaseModel):
    name : str
    description : str | None = None
    price : float
    tax : float | None = None

items = []
@app.post("/items")
def create_item(item : Item):
    items.append(item)
    return item

@app.get("/items")
def get_items():
    return items


@app.post("/items/fss")
async def create_items(item : Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax" : price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
def update_item(item_id : int, item : Item, q : str | None = None):
    result = {"item_id":item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result

