from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .models import Order
from .schemas import *
from src.products.schemas import *
from src.orders.controllers import _create_order, _get_order_items
from src.orders.controllers import get_object_by_id

router = APIRouter(
    prefix='/orders'
)


# @router.post('/', response_model=FullOrderResponse)
# def create_order(data: Products, db: Session = Depends(get_db)):
#     return _create_order(data, db)


# @router.get('/', response_model=OrderResponseList)
# def order_list(db: Session = Depends(get_db)):
#     orders = db.query(Order).order_by(Order.created)

#     order_list = [OrderResponse.model_validate(order) for order in orders]
    
#     return OrderResponseList(orders=order_list)


# @router.get('/{order_id}', response_model=FullOrderResponse)
# def get_order(order_id: int, db: Session = Depends(get_db)):
#     order = get_object_by_id(db, Order, order_id)

#     order_items, price = _get_order_items(order)

#     return {
#         'id': order.id,
#         'created': order.created,
#         'state': order.state,
#         'total_price': price,
#         'order_items': order_items
#     }


# @router.patch('/{order_id}/status', response_model=OrderResponse)
# def update_order_status(order_id: int, request: UpdateOrderState, db: Session = Depends(get_db)):
#     order = get_object_by_id(db, Order, order_id)

#     order.state = request.state
#     db.commit()

#     return order