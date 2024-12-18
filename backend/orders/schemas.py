from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict

from backend.orders.models import OrderState


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


class Order(BaseModel):
    id: int
    created: datetime
    state: OrderState

    model_config = ConfigDict(from_attributes=True)


class ProductItem(BaseModel):
    id: int
    count: int

    model_config = ConfigDict(from_attributes=True)
