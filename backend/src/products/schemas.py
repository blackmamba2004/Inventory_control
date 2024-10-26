from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class Product(BaseModel):
    title: str
    description: str
    price: float
    count: int


class CreateProduct(Product):
    pass


class UpdateProduct(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    count: Optional[int] = None


class FullProductResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    count: int

    model_config = ConfigDict(from_attributes=True)