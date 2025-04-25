from fastapi import APIRouter, Depends,status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from sqlalchemy.orm import selectinload

from app import schemas
from app.backend.db_depends import get_db
from sqlalchemy import select, insert

from app.models import Category
from app.schemas import CategoryCreate

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get('/')
async def get_categories(db: Annotated[AsyncSession, Depends(get_db)]):
    result=await db.execute(select(Category).options(selectinload(Category.products)))
    return result.scalars().all()
@router.post('/',status_code=status.HTTP_201_CREATED)
async def add_categories(category: CategoryCreate, db: Annotated[AsyncSession,Depends(get_db)]):
    categories= await db.execute(insert(Category).values(name=category.name))
    await db.commit()

    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}