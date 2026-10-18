# this file is used to make connection between database and my project
# Its job is only to establish the connection between FastAPI and PostgreSQL.

from sqlalchemy import create_engine;#make connection between database and fast api

from sqlalchemy.orm import sessionmaker# help to perform crud opertaion on database
from dotenv import load_dotenv
load_dotenv()
import os
from sqlalchemy.orm import declarative_base#The Base acts as the common foundation for your ORM model classes.
database_url=os.getenv("DATABASE_URL")
if database_url:
    if database_url.startswith("postgresql+psycopg://"):
        database_url = database_url.replace(
            "postgresql+psycopg://",
            "postgresql+psycopg2://",
            1
        )
    elif database_url.startswith("postgresql://"):
        database_url = database_url.replace(
            "postgresql://",
            "postgresql+psycopg2://",
            1
        )


engine=create_engine(url=database_url)
# So whenever we need a database session, we can do:

# db = SessionLocal()
Sessionlocal=sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)
base=declarative_base()
# we need session to perform database operation db.add(),db.delete(),db.commit()
def get_db():
    db=Sessionlocal()
    try:
        yield db
    finally:
        db.close()