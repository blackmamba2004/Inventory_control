from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.database import with_session
from backend.dao.base import BaseDAO
from backend.orders.models import Order, OrderItem
from backend.products.dao import ProductDAO
from backend.products.models import Product
from backend.orders.schemas import ProductItem


class OrderDAO(BaseDAO):
    model = Order

    @classmethod
    @with_session
    async def create_order(cls, session: AsyncSession):
        order = Order(created=datetime.now())
        session.add(order)
        await session.flush()
        return order

    @classmethod
    @with_session
    async def create(cls, session: AsyncSession, data: list[ProductItem]):
        """Метод, использующий транзакцию для создания заказа"""
        async with session.begin():
            order = await cls.create_order(session)

            total_price, order_items = await cls.add_order_items(
                session, order.id, data
            )

            return {
                "id": order.id,
                "created": order.created,
                "state": order.state,
                "total_price": total_price,
                "order_items": order_items,
            }

    @classmethod
    async def add_order_items(
        cls, session: AsyncSession, order_id: int, data: list[ProductItem]
    ):
        order_items_responses = []
        total_price = 0

        product_ids = [product.id for product in data]

        products = await ProductDAO.find_all_by_id(session, product_ids)

        products_dict = {product.id: product for product in products}

        for item in data:
            product = products_dict.get(item.id)

            requested_count = item.count

            await ProductDAO.check_count(product, requested_count)
            await OrderItemDAO.create_order_item(
                session, order_id, product.id, requested_count
            )

            order_items_responses.append(
                OrderItemDAO.build_order_item_json(product, requested_count)
            )

            total_price += requested_count * product.price

        return total_price, order_items_responses

    @classmethod
    @with_session
    async def find_full_order(cls, session: AsyncSession, order_id: int):
        order = await cls.load_order_by_id(session, order_id=order_id)
        return cls.build_full_order_json(order)

    @classmethod
    @with_session
    async def load_order_by_id(cls, session: AsyncSession, order_id: int):
        query = (
            select(Order)
            .options(
                joinedload(Order.order_items).joinedload(OrderItem.product)
            )
            .where(Order.id == order_id)
        )
        result = await session.execute(query)
        return result.unique().scalar_one_or_none()

    @classmethod
    def build_full_order_json(cls, order: Order):
        order_items_responses = []
        total_price = 0

        for order_item in order.order_items:

            total_price += order_item.product.price * order_item.count

            order_items_responses.append(
                OrderItemDAO.build_order_item_json(
                    order_item.product, order_item.count
                )
            )

        return {
            "id": order.id,
            "created": order.created,
            "state": order.state,
            "total_price": total_price,
            "order_items": order_items_responses,
        }


class OrderItemDAO(BaseDAO):
    model = OrderItem

    @classmethod
    async def create_order_item(
        cls,
        session: AsyncSession,
        order_id: int,
        product_id: int,
        requested_count: int,
    ):
        order_item = OrderItem(
            order_id=order_id, product_id=product_id, count=requested_count
        )
        session.add(order_item)

    @classmethod
    def build_order_item_json(cls, product: Product, count: int):
        return {
            "product_id": product.id,
            "title": product.title,
            "price": product.price,
            "count": count,
        }
