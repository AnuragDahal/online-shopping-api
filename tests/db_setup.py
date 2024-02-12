from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, StaticPool
import pytest
from sqlalchemy.ext.declarative import declarative_base

TESTDATABASE_URL = "sqlite:///./test_PizzaShop.db"


engine = create_engine(TESTDATABASE_URL,
                       connect_args={"check_same_thread": False},
                       poolclass=StaticPool)

TestingSessionLocal = sessionmaker(
    autoflush=False, autocommit=False, bind=engine
)


Base = declarative_base()
