#  models.Product a Pydantic model that I can use to validate and serialize the API response?
from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from database import base ,engine,get_db

from model import Product
import model
import schemas
base.metadata.create_all(bind=engine)
app=FastAPI()
@app.get('/products',response_model=list[schemas.Product])
# "Before running get_products, I need to get a database session."
# So FastAPI calls:
# get_db()
def allproducts(db:Session=Depends(get_db)):
    products=db.query(model.Product).all() #this line is similar to select*from product
    return products


@app.post('/add',response_model=schemas.Product)
def add_product(product:schemas.Product,db:Session=Depends(get_db)):
    new_product=model.Product(
        
        name=product.name,
        image=product.image,
        price=product.price,
        rating=product.rating,
        reviews=product.reviews,
        category=product.category
    )
    db.add(new_product)
    db.commit()
    return new_product


@app.get('/similarproduct/{name}',response_model=list[schemas.Product])
def all_name(name:str,db:Session=Depends(get_db)):
    products=db.query(model.Product).filter(model.Product.name.ilike(f"%{name}%")).all()
    return products

@app.get('/category/{category}',response_model=list[schemas.Product])
def catefilter(category:str,db:Session=Depends(get_db)):
    products=db.query(model.Product).filter(model.Product.category==category).all()
    return products
@app.put('/update/{id}')
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
    db.commit()

    return {'message':'update new value'}
@app.delete('/delete/{id}')
def delete_product(id:int,db:Session=Depends(get_db)):
    existing_product=db.query(model.Product).filter(model.Product.id==id).first()
    if not existing_product:
        raise HTTPException(status_code=404,detail={'message':'product not found'})
    db.delete(existing_product)
    db.commit()
    return {
        'message':'product delete successfully'
    }