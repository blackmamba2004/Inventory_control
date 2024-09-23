from pydantic import BaseModel
from datetime import datetime
from typing import List
from .models import *


class OrderItem(BaseModel):
    """db_table = order_item"""
    product_id: int
    count: int

    class Config:
        orm_mode = True
        from_attributes=True


class OrderResponse(BaseModel):
    """db_table = order"""
    order_id: int
    created: datetime
    state: OrderState
    order_items: List[OrderItem]


class OrderItems(BaseModel):
    order_items: List[OrderItem]