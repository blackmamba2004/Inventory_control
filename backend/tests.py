import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.routes.orders.controllers import get_object_by_id
from src.routes.products.models import Product
from src.routes.products.schemas import FullProductResponse

from settings.database import SessionLocal

from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


@pytest.fixture()
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def drop_db_counter(db: Session):
    db.execute(text("ALTER SEQUENCE product_id_seq RESTART WITH 10;"))
    db.commit()


def test_product_list():
    
    response = client.get('/products/')
    assert response.status_code == 200
    assert isinstance(response.json()['products'], list)


def test_get_product(db: Session):
    
    drop_db_counter(db)

    product_data = {
        'title': 'Nike',
        'description': 'кроссовки',
        'price': 45.99,
        'count': 27
    }

    new_product = Product(**product_data)
    db.add(new_product)
    db.commit()
    
    product_id = new_product.id
    response = client.get(f'/products/{product_id}/')
    
    assert response.status_code == 200
    assert response.json() == {'id': product_id, **product_data}

    db.delete(new_product)
    db.commit()


def test_get_product_with_error():
    product_id = 100
    response = client.get(f'/products/{product_id}/')
    assert response.status_code == 404


def test_create_product(db: Session):

    drop_db_counter(db)

    product_data = {
        'title': 'Nike',
        'description': 'кроссовки',
        'price': 45.99,
        'count': 27
    }

    response = client.post('/products/', json=product_data)
    new_product = get_object_by_id(db, Product, response.json()['id'], test_flag=True)

    assert response.status_code == 201
    assert response.json() == FullProductResponse.model_validate(new_product).model_dump()

    db.delete(new_product)
    db.commit()


def test_put_product(db: Session):

    drop_db_counter(db)

    product_data = {
        'title': 'Nike',
        'description': 'кроссовки',
        'price': 45.99,
        'count': 27
    }

    new_product = Product(**product_data)
    db.add(new_product)
    db.commit()

    changed_data = {
        'title': 'Nike',
        'description': 'кроссовки',
        'price': 35.99,
        'count': 27
    }

    response = client.put(f'/products/{new_product.id}', json=changed_data)
    db.refresh(new_product)

    assert response.status_code == 200
    assert product_data['price'] != new_product.price

    db.delete(new_product)
    db.commit()


def test_delete_product(db: Session):
    drop_db_counter(db)

    product_data = {
        'title': 'Nike',
        'description': 'кроссовки',
        'price': 45.99,
        'count': 27
    }

    new_product = Product(**product_data)
    db.add(new_product)
    db.commit()

    response = client.delete(f'/products/{new_product.id}')

    assert response.status_code == 200