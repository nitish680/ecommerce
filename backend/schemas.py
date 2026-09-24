from pydantic import BaseModel, ConfigDict


class Product(BaseModel):
    id: int 
    name: str
    image: str
    price: float
    rating: float
    reviews: int
    category: str

    model_config = ConfigDict(from_attributes=True)