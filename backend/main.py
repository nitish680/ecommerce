# notes:
# returns every product at once.

# That works for a few products, but imagine your store has 10,000 products. Sending all 10,000 in one response is inefficient.

# Pagination means:

# 10000 products
#       ↓
# Page 1 → 10 products
# Page 2 → 10 products
# Page 3 → 10 products
# ...

# We'll use two query parameters:

# skip → how many products to skip
# limit → how many products to return















from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
#  models.Product a Pydantic model that I can use to validate and serialize the API response?
from fastapi import FastAPI,Depends,HTTPException,status,Query
from sqlalchemy.orm import Session
from database import base ,engine,get_db

from model import Product
import model
import schemas
pwd_context=CryptContext(
    schemes=["bycrypt"],
    deprecated="auto"
)
base.metadata.create_all(bind=engine)
app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
@app.get('/products',response_model=list[schemas.ReturnProduct])
# "Before running get_products, I need to get a database session."
# So FastAPI calls:
# get_db()
def allproducts(skip:int = Query(0,ge=0),limit:int =Query(10,ge=1,le=100),db:Session=Depends(get_db)):
    products=db.query(model.Product).all() #this line is similar to select*from product
    return products


@app.post('/add',response_model=schemas.ReturnProduct,status_code=status.HTTP_201_CREATED)
def add_product(product:schemas.Product,db:Session=Depends(get_db)):
    new_product=model.Product(
        
        name=product.name,
        image=product.image,
        price=product.price,
        rating=product.rating,
        reviews=product.reviews,
        category=product.category
    )
    try:
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500,detail="failed to create the product")
    return new_product


@app.get('/similarproduct/{name}',response_model=list[schemas.ReturnProduct],status_code=status.HTTP_200_OK)
def all_name(name:str,skip:int =Query(0,ge=0),limit:int =Query(10,ge=1,le=10),db:Session=Depends(get_db)):
    products=db.query(model.Product).filter(model.Product.name.ilike(f"%{name}%")).all()
    return products

@app.get('/product/{id}',response_model=schemas.ReturnProduct)
def find_by_id(id:int,db:Session=Depends(get_db)):
    product=db.query(model.Product).filter(model.Product.id==id).first()
    if not product:
        raise HTTPException(status_code=404,detail={'message':'product not found'})
    return product
@app.post("/register")
def register(user:schemas.CreateUser,db:Session=Depends(get_db)):
    existing_user=db.query(model.Users.email==user.email).first()
    existing_phone=db.query(model.Users.phone_no==user.phone_no).first()

    if existing_user:
        raise HTTPException(status_code=400,detail="email already exists")
    if existing_phone:
        raise HTTPException(status_code=400,detail="mobile no already exist")
@app.post("/orders")
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):

    total_amount = 0
    order_items = []

    for item in order.items:

        product = db.query(model.Product).filter(
            model.Product.id == item.product_id
        ).first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product with id {item.product_id} not found"
            )

        item_total = product.price * item.quantity
        total_amount += item_total

        order_item = model.OrderItem(
            order_id=order.order_id,
            product_id=product.id,
            quantity=item.quantity,
            total=item_total
        )

        order_items.append(order_item)

    new_order = model.Order(
        order_id=order.order_id,
        customer_name=order.customer_name,
        phone=order.phone,
        address=order.address,
        total_amount=total_amount,
        status="Placed"
    )

    try:
        db.add(new_order)

        for item in order_items:
            db.add(item)

        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return {
        "message": "Order placed successfully",
        "order_id": new_order.order_id,
        "total_amount": new_order.total_amount,
        "status": new_order.status
    }
@app.get('/category/{category}',response_model=list[schemas.ReturnProduct])
def catefilter(category:str,skip:int =Query(0,ge=0),limit:int=Query(10,ge=0,le=10),db:Session=Depends(get_db)):
    products=db.query(model.Product).filter(model.Product.category==category).all()
    return products
@app.put('/update/{id}',response_model=schemas.ReturnProduct)
def update_record(id:int,product:schemas.Product,db:Session=Depends(get_db)):
    existing_product=db.query(model.Product).filter(model.Product.id==id).first()
    if not existing_product:
        raise HTTPException(status_code=404,detail={'message':'product not found'})
    existing_product.name=product.name
    existing_product.image=product.image
    existing_product.price = product.price
    existing_product.rating = product.rating
    existing_product.reviews = product.reviews
    existing_product.category = product.category
    try:

        db.commit()
        db.refresh(existing_product)

    except Exception:
        raise HTTPException(status_code=500,detail="failed to update the product")

    return existing_product
@app.delete('/delete/{id}')
def delete_product(id:int,db:Session=Depends(get_db)):
    existing_product=db.query(model.Product).filter(model.Product.id==id).first()
    if not existing_product:
        raise HTTPException(status_code=404,detail={'message':'product not found'})
    try:
        db.delete(existing_product)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500,detail="failed to delete the product")


    return {
        'message':'product delete successfully',
        'id':id,
        'name':existing_product.name
    }