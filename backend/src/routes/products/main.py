from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.util.db_dependency import get_db
from .models import Product
from .schemas import *


router = APIRouter(
    prefix='/products'
)


@router.post('/', response_model=ProductResponse)
def create_product(product: CreateProduct, db: Session = Depends(get_db)):
    new_product = Product(**product.model_dump())
    db.add(new_product)
    db.commit()

    return new_product


@router.get('/', response_model=ProductResponseList)
def product_list(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    product_responses = [ProductResponse.model_validate(product) for product in products]

    return ProductResponseList(products=product_responses)


@router.get('/{product_id}', response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product


@router.put('/{product_id}', response_model=ProductResponse)
def put_product(product_id: int, updated_data: UpdateProduct, db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in updated_data.model_dump().items():
        setattr(product, key, value)

    db.commit()
    return product


@router.delete('/{product_id}')
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()

    return product