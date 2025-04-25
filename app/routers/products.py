from fastapi import APIRouter, Depends,status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from sqlalchemy.orm import selectinload

from app import schemas
from app.backend.db_depends import get_db
from sqlalchemy import select, insert

from app.models import Product
from app.schemas import ProductCreate

router = APIRouter(prefix="/products", tags=["products"])

@router.get('/')
async def get_products(db: Annotated[AsyncSession, Depends(get_db)]):
    result= await db.execute(select(Product).options(selectinload(Product.categories)))
    return result.scalars().all()
@router.post('/',status_code=status.HTTP_201_CREATED)
async def add_product(category: ProductCreate, db: Annotated[AsyncSession,Depends(get_db)]):
    categories= await db.execute(insert(Product).values(name=category.name))
    await db.commit()

    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}