from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from src.util.db_dependency import get_db
from .models import Order, OrderItem as OrderItemSQL
from .schemas import *
from src.routes.products.schemas import *
from src.routes.products.models import Product
from src.routes.orders.controllers import _create_order

router = APIRouter(
    prefix='/orders'
)

@router.post('/', response_model=OrderResponse)
def create_order(data: Products, db: Session = Depends(get_db)):
    return _create_order(data, db)


# @router.post('/{order_id}', response_model=OrderResponse)
@router.post('/{order_id}', response_model=OrderItems)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')
    
    order_items = order.order_items

    order_items_responses = [OrderItem.model_validate(order_item) 
                             for order_item in order_items]
    
    return OrderItems(order_items=order_items_responses)