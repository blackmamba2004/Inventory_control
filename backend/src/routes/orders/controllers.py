from fastapi import HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from src.routes.orders.models import *
from src.routes.products.models import *
from src.routes.products.schemas import Products


def create_new_order(db: Session):
    new_order = Order(created = datetime.now())
    db.add(new_order)
    db.commit()
    return new_order


def get_product_by_id(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, 
                            detail='Product with id {product_id} not found')
    return product


def check_count(product: Product, requested_count: int):
    if product.count < requested_count:
        raise HTTPException(status_code=404, 
                            detail='Error')


def create_order_item(db: Session, order_id: int, product: Product, requested_count: int):
    order_item = OrderItem(order_id=order_id, product_id=product.id, count=requested_count)

    product.count -= requested_count
    db.add(order_item)


def _create_order(data: Products, db: Session):

    new_order = create_new_order(db)

    order_items = []

    for product in data.products:
        product_id = product.id
        requested_count = product.count

        product = get_product_by_id(db, product_id)

        check_count(product, requested_count)

        create_order_item(db, new_order.id, product, requested_count)

        order_items.append({
            'product_id': product_id,
            'title': product.title,
            'count': requested_count
        })
    
    db.commit()
    return {
        'order_id': new_order.id,
        'created': new_order.created,
        'state': new_order.state, 
        'order_items': order_items
    }