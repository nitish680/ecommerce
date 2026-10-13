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
from dotenv import load_dotenv
import os
from datetime import timedelta,timezone,datetime
import jwt
load_dotenv()
secret_key=os.getenv("JWT_SECRETS_KEY")
ALGORITHM='HS256'
ACCESS_TOKEN_EXPIRY_MINUTES=30

from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
#  models.Product a Pydantic model that I can use to validate and serialize the API response?
from fastapi import FastAPI,Depends,HTTPException,status,Query
from sqlalchemy.orm import Session
from database import base ,engine,get_db
from fastapi import Header
from model import Product
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import model
import schemas
security=HTTPBearer()
pwd_context=CryptContext(
    schemes=["bcrypt"],
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
def create_token(user_id:int):
    expiry=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    payload={
        "sub":str(user_id),
        "exp":expiry
    }
    token=jwt.encode(
        payload,
        secret_key,
        algorithm=ALGORITHM

    )
    return token

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return int(user_id)

    except (jwt.InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

def get_current_admin(user_id:int=Depends(get_current_user),db:Session=Depends(get_db)):
    existing_user=db.query(model.Users).filter(model.Users.id==user_id).first()
    if existing_user is None:
        raise HTTPException(status_code=401,detail="user not found")
    if existing_user.role.lower()!="admin":
        raise HTTPException(status_code=403,detail="Admin acess required")
    return existing_user
@app.get("/protected")
def protected_route(user_id: int = Depends(get_current_user)):
    return {
        "message": "You are authenticated!",
        "user_id": user_id
    }
# user_id → Who is the user?



# expire → When does the token expire?



# payload → What information goes into the token?



# jwt.encode() → Creates the signed token.



@app.get('/products',response_model=list[schemas.ReturnProduct])
# "Before running get_products, I need to get a database session."
# So FastAPI calls:
# get_db()
def allproducts(skip:int = Query(0,ge=0),limit:int =Query(10,ge=1,le=100),db:Session=Depends(get_db)):
    products=db.query(model.Product).all() #this line is similar to select*from product
    return products


@app.post('/add',response_model=schemas.ReturnProduct,status_code=status.HTTP_201_CREATED)
def add_product(product:schemas.Product,db:Session=Depends(get_db),current_admin:model.Users=Depends(get_current_admin)):
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
    existing_user=db.query(model.Users).filter(model.Users.email==user.email).first()
    existing_phone=db.query(model.Users).filter(model.Users.phone_no==user.phone_no).first()

    if existing_user:
        raise HTTPException(status_code=400,detail="email already exists")
    if existing_phone:
        raise HTTPException(status_code=400,detail="mobile no already exist")
    hashed_password=pwd_context.hash(user.password)
    new_user=model.Users(
        name=user.name,
        email=user.email,
        phone_no=user.phone_no,
        password=hashed_password
    )
    try:
        db.add(new_user)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=505,detail="failed to add new user")
    return{
        "message":"User Registered Successfully ",
        "id":new_user.id
    }
@app.post("/orders")
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db),user_id:int =Depends(get_current_user)):

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
        customer_id=user_id,
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
@app.post("/login")
def login(user:schemas.login,db:Session=Depends(get_db)):
    existing_user=db.query(model.Users).filter(model.Users.email==user.email).first()
    if not existing_user:
        raise HTTPException(status_code=401,detail="invalid email  or password")
    password_valid=pwd_context.verify(user.password,existing_user.password)
    if not password_valid:
        raise HTTPException(
            status_code=404,
            detail="invalid email or password"
        )
    token=create_token(existing_user.id)

    return {
        "message":"login successfully",
        "id":existing_user.id,
        "name":existing_user.name,
        "role":existing_user.role,
        "token":token,
        "type":"bearer"
    }

@app.get("/orders/history")
def get_order_history(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)):
    orders = (
        db.query(model.Order)
        .filter(model.Order.customer_id == user_id)
        .order_by(model.Order.created_time.desc())
        .all()
    )

    history = []

    for order in orders:
        history.append({
            "order_id": order.order_id,
            "customer_name": order.customer_name,
            "created_time": order.created_time,
            "total_amount": order.total_amount,
            "status": order.status,
            "items": [
                {
                    "product_id": item.product_id,
                    "product_name": item.product.name,
                    "quantity": item.quantity,
                    "total": item.total
                }
                for item in order.items
            ]
        })

    return {"orders": history}
