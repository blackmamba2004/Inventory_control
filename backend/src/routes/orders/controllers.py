from fastapi import HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from src.routes.orders.models import *
from src.routes.products.models import *
from src.routes.products.schemas import Products
from src.routes.orders.schemas import OrderItem as OrderItemPy


def create_new_order(db: Session):
    new_order = Order(created = datetime.now())
    db.add(new_order)
    db.commit()
    return new_order


def get_object_by_id(db: Session, model, object_id: int):
    object = db.query(model).filter(model.id == object_id).first()

    if not object:
        raise HTTPException(status_code=404, 
                            detail=f'{model.__name__}'
                            f' with {model.__name__.lower()}_id = {object_id} not found')
    return object


def check_count(product: Product, requested_count: int):
    if product.count < requested_count:
        raise HTTPException(status_code=404, 
                            detail=f'The product with id = {product.id} is not in stock or it is not enough')


def create_order_item(db: Session, order_id: int, product: Product, requested_count: int):
    order_item = OrderItem(order_id=order_id, product_id=product.id, count=requested_count)

    product.count -= requested_count
    db.add(order_item)


def _create_order(data: Products, db: Session):

    new_order = create_new_order(db)

    order_items = []

    total_price: float = 0

    for product in data.products:
        product_id = product.id
        requested_count = product.count

        product = get_object_by_id(db, Product, product_id)

        check_count(product, requested_count)

        create_order_item(db, new_order.id, product, requested_count)

        order_items.append({
            'product_id': product_id,
            'title': product.title,
            'price': product.price*requested_count,
            'count': requested_count
        })

        total_price += requested_count * product.price
    
    db.commit()
    return {
        'id': new_order.id,
        'created': new_order.created,
        'state': new_order.state,
        'total_price': total_price,
        'order_items': order_items
    }


def _get_order_items(order: Order):
    order_items = order.order_items

    order_items_responses = []

    total_price: float = 0

    for order_item in order_items:

        order_item_product_price = order_item.product.price
        order_item_count = order_item.count

        total_price += order_item_product_price * order_item_count
        price = order_item_product_price * order_item_count

        item_data = {
            'product_id': order_item.product_id,
            'title': order_item.product.title, 
            'price': price,
            'count': order_item_count
        }

        validated_data = OrderItemPy.model_validate(item_data)
        order_items_responses.append(validated_data)
    
    return order_items_responses, total_price