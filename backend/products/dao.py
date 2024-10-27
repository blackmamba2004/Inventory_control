from fastapi import HTTPException

from backend.dao.base import BaseDAO
from backend.products.models import Product


class ProductDAO(BaseDAO):
    model = Product

    @classmethod
    async def check_count(cls, product: Product, requested_count: int):
        if product.count < requested_count:
            raise HTTPException(
                status_code=404,
                detail=f"The product with id = {product.id} is not in stock or it is not enough",
            )
        product.count -= requested_count
