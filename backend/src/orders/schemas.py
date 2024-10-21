from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List
from .models import *


"""
    Схема обновления состояния заказа
"""
class UpdateOrderState(BaseModel):
    state: OrderState


"""
    Элемент заказа
"""
class OrderItem(BaseModel):
    product_id: int
    title: str
    price: float
    count: int


"""
    Схема полного отображения заказа
"""
class FullOrderResponse(BaseModel):
    id: int
    created: datetime
    state: OrderState
    total_price: float
    order_items: List[OrderItem]


"""
    Ниженаходящиеся схемы для отображения в списке заказов 
    и для отображения смены состояния заказа
"""
class OrderResponse(BaseModel):
    id: int
    created: datetime
    state: OrderState

    model_config = ConfigDict(from_attributes=True)


class OrderResponseList(BaseModel):
    orders: List[OrderResponse]