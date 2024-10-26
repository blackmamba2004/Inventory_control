from backend.database import Base
from backend.src.orders.models import OrderItem
from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.orm import relationship, Relationship


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    count = Column(Integer, nullable=False, default=0)

    #один ко многим 
    order_items = relationship('OrderItem', back_populates='product')
