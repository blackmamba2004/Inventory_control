from pydantic import BaseModel, ConfigDict
from typing import List


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


class FullProductResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    count: int

    model_config = ConfigDict(from_attributes=True)


class ProductResponse(BaseModel):
    id: int
    title: str
    price: float
    count: int

    model_config = ConfigDict(from_attributes=True)


class ProductResponseList(BaseModel):
    products: List[ProductResponse]


"""
    Ниженаходящиеся схемы относятся к логике 
    обработки заказов и применяются в orders/main.py
"""
class ProductItem(BaseModel):
    id: int
    count: int

    model_config = ConfigDict(from_attributes=True)


class Products(BaseModel):
    products: List[ProductItem]