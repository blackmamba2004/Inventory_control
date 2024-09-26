from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from settings.db_dependency import get_db
from src.routes.orders.controllers import get_object_by_id
from .models import Product
from .schemas import *


router = APIRouter(
    prefix='/products'
)


@router.post('/', response_model=FullProductResponse, status_code=201)
def create_product(product: CreateProduct, db: Session = Depends(get_db)):
    new_product = Product(**product.model_dump())
    db.add(new_product)
    db.commit()

    return new_product


@router.get('/', response_model=ProductResponseList)
def product_list(db: Session = Depends(get_db)):
    products = db.query(Product).order_by(Product.id)
    product_responses = [ProductResponse.model_validate(product) for product in products]

    return ProductResponseList(products=product_responses)


@router.get('/{product_id}', response_model=FullProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = get_object_by_id(db, Product, product_id)
    
    return product


@router.put('/{product_id}', response_model=FullProductResponse, status_code=200)
def put_product(product_id: int, updated_data: UpdateProduct, db: Session = Depends(get_db)):
    product = get_object_by_id(db, Product, product_id)

    for key, value in updated_data.model_dump().items():
        setattr(product, key, value)

    db.commit()
    return product


@router.delete('/{product_id}', response_model=FullProductResponse, status_code=200)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = get_object_by_id(db, Product, product_id)
    
    db.delete(product)
    db.commit()

    return product