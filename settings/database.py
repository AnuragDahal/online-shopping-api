from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from env_utils import Environment


env=Environment()

url=env.DATABASE_URL
print(url)

engine = create_engine(url)

SessionLocal = sessionmaker(bind=engine, autoflush=True)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
