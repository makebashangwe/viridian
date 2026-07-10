import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv() #loads .env file so python can read DATABASE_URL

DATABASE_URL = os.getenv("DATABASE_URL") #pulls the DB URL connection string

if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(DATABASE_URL) #creates the connection engine to postgresql

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base() #where future DB tables will inherit from

def get_db():#gives each route  temporary access to the database, then closes the connection after the request finishes.
    db = SessionLocal() #creates database sessions / conversastions with the DB
    try:
        yield db
    finally:
        db.close()