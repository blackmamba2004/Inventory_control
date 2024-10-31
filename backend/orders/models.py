from enum import Enum

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import relationship

from backend.database import Base


class OrderState(Enum):
    SENT = "sent"
    DELIVERED = "delivered"
    IN_PROCESS = "in_process"


class Order(Base):
    """
    Таблица заказов
    """

    __tablename__ = "order"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DateTime)
    state = Column(PgEnum(OrderState), nullable=False, default=OrderState.IN_PROCESS)

    # один ко многим
    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    """
    Таблица элементов заказа
    """

    __tablename__ = "order_item"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    count = Column(Integer)

    # многие ко одному
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
