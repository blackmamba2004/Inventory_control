from pydantic import BaseModel
from datetime import datetime
from typing import List
from .models import *


class UpdateOrderState(BaseModel):
    state: OrderState


class OrderItem(BaseModel):
    product_id: int
    title: str
    price: float
    count: int


class FullOrderResponse(BaseModel):
    id: int
    created: datetime
    state: OrderState
    total_price: float
    order_items: List[OrderItem]


class OrderResponse(BaseModel):
    id: int
    created: datetime
    state: OrderState

    class Config:
        from_attributes = True


class OrderResponseList(BaseModel):
    orders: List[OrderResponse]