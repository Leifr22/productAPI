from fastapi import FastAPI
from app.routers import products,categories,pairs
from app.backend.db import engine, Base
app=FastAPI()
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(products.router)
app.include_router(categories.router)
app.include_router(pairs.router)

@app.get('/')
async def welcome():
    return {'message': 'Product-Category API'}