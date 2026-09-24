# in this file  We're defining the structure of a database table.
from database import base
from sqlalchemy import Column,Integer,String,Float
class Product(base):
    __tablename__='products'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    image=Column(String,nullable=False)
    price=Column(Float,nullable=False)
    rating=Column(Float)
    reviews = Column(Integer)
    category = Column(String, nullable=False)
