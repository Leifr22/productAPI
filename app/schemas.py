from pydantic import BaseModel,ConfigDict
from typing import List, Optional

class ProductCreate(BaseModel):
    name: str

class Product(ProductCreate):
    id: int
    categories: List['Category'] = []
    model_config = ConfigDict(from_attributes=True)

class CategoryCreate(BaseModel):
    name: str

class Category(CategoryCreate):
    id: int
    products: List[Product] = []
    model_config = ConfigDict(from_attributes=True)

class PairCreate(BaseModel):
    product_id: int
    category_id: int


class Pair(BaseModel):
    product: Optional[str] = None
    category: Optional[str] = None