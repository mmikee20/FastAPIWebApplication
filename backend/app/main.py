from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import schema, crud, database
from app.database import get_db


@asynccontextmanager
async def get_db_session():
    async with get_db() as session:
        yield session


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}

@app.on_event("startup")
async def startup():
    await database.init_db()

@app.get("/items/", response_model=list[schema.Item])
async def list_items(db: AsyncSession = Depends(get_db)):
    return await crud.get_items(db)

@app.post("/items/", response_model=schema.Item)
async def create_item(item: schema.ItemCreate, db: AsyncSession = Depends(get_db_session)):
    return await crud.create_item(db, item)

@app.get("/items/{item_id}", response_model=schema.Item)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db_session)):
    item = await crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=schema.Item)
async def update_item(item_id: int, item: schema.ItemCreate, db: AsyncSession = Depends(get_db_session)):
    return await crud.update_item(db, item_id, item)

@app.delete("/items/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db_session)):
    return await crud.delete_item(db, item_id)

