# Adding product → ID is NOT required
# Returning product → ID IS required


from pydantic import BaseModel, ConfigDict,Field


class Product(BaseModel):
    name: str=Field(min_length=2,max_length=100)
    image: str=Field(min_length=2)
    price: float=Field(gt=0)
    rating: float=Field(ge=0,le=5)
    reviews: int =Field(ge=0)
    category: str=Field(min_length=2,max_length=50)

    model_config = ConfigDict(from_attributes=True)
class ReturnProduct(BaseModel):
    id:int
    name: str
    image: str
    price: float
    rating: float
    reviews: int
    category: str

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    order_id: str
    customer_name: str = Field(min_length=2, max_length=100)
    address: str = Field(min_length=5, max_length=300)
    items: list[OrderItemCreate]
    phone:str
class CreateUser(BaseModel):
    name:str
    email:str
    phone_no:str
    password:str