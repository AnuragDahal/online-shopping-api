from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from .env_utils import Environment
from typing import Annotated
from fastapi import Depends


env = Environment()

url = env.DATABASE_URL

engine = create_engine(url)

SessionLocal = sessionmaker(bind=engine, autoflush=True)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
