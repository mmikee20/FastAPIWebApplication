from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import schema, crud, database

""" from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}



@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict """


app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.init_db()

@app.post("/items/", response_model=schema.Item)
async def create_item(item: schema.ItemCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.create_item(db, item)

@app.get("/items/", response_model=list[schema.Item])
async def list_items(db: AsyncSession = Depends(database.get_db)):
    return await crud.get_items(db)

@app.get("/items/{item_id}", response_model=schema.Item)
async def get_item(item_id: int, db: AsyncSession = Depends(database.get_db)):
    item = await crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=schema.Item)
async def update_item(item_id: int, item: schema.ItemCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.update_item(db, item_id, item)

@app.delete("/items/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(database.get_db)):
    return await crud.delete_item(db, item_id)

