from sqlalchemy import Column, Float, Integer, String, Text
from sqlalchemy.orm import relationship

from backend.database import Base
from backend.orders.models import OrderItem


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    count = Column(Integer, nullable=False, default=0)

    # один ко многим
    order_items = relationship("OrderItem", back_populates="product")
