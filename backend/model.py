# in this file  We're defining the structure of a database table.
from database import base
from datetime import datetime
from sqlalchemy import Column,Integer,String,Float,ForeignKey,DateTime
from sqlalchemy.orm import relationship

class Product(base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    image = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    rating = Column(Float)
    reviews = Column(Integer)
    category = Column(String, nullable=False)

    order_items = relationship("OrderItem", back_populates="product")


class Order(base):
    __tablename__ = "orders"

    order_id = Column(String, primary_key=True)
    customer_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone=Column(String,nullable=True)
    total_amount = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    created_time = Column(DateTime, default=datetime.utcnow)

    items = relationship("OrderItem", back_populates="order")


class OrderItem(base):
    __tablename__ = "orderitem"

    id = Column(Integer, primary_key=True)
    order_id = Column(String, ForeignKey("orders.order_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    total = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

class Users(base):
    __tablename__="user"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    phone_no=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False,unique=True)
    role=Column(String,default="customer",nullable=False)