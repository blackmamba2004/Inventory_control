from pydantic import BaseModel
from typing import List


class ProductItem(BaseModel):
    id: int
    count: int


class CreateProduct(BaseModel):
    title: str
    description: str
    price: float
    count: int


class UpdateProduct(BaseModel):
    title: str
    description: str
    price: float
    count: int


class ProductResponse(BaseModel):
    title: str
    description: str
    price: float
    count: int

    class Config:
        orm_mode = True
        from_attributes=True


class ProductResponseList(BaseModel):
    products: List[ProductResponse]


class Products(BaseModel):
    products: List[ProductItem]