from typing import Annotated

from fastapi import APIRouter, Depends,status,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, union_all, text,insert

from app.models import product_category
from app.schemas import Pair, PairCreate
from app.backend.db_depends import get_db

router = APIRouter(prefix="/pairs", tags=["pairs"])

@router.get("/")
async def read_pairs(db: Annotated[AsyncSession,Depends(get_db)]):
    query = text("""
        SELECT p.name as product, c.name as category
        FROM products p
        LEFT JOIN product_category pc ON p.id = pc.product_id
        LEFT JOIN categories c ON pc.category_id = c.id
        UNION
        SELECT NULL, name FROM categories
        WHERE NOT EXISTS (
            SELECT 1 FROM product_category WHERE category_id = categories.id
        )
    """)
    result = await db.execute(query)
    return result.mappings().all()
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_pair(
    pair: PairCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        await db.execute(
            insert(product_category).values(
                product_id=pair.product_id,
                category_id=pair.category_id
            )
        )
        await db.commit()
        return {"message": "Pair created successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product or category ID"
        )