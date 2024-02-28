import pytest
from . import db_setup
from sqlalchemy import Integer, String, Boolean, ForeignKey, DATETIME
from fastapi import Depends
from fastapi.testclient import TestClient
from routes.users import router
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import Integer, String, Boolean, DateTime
from .db_setup import Base, engine, TestingSessionLocal
client = TestClient(router)


class User(Base):

    __tablename__ = "mockdb"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    time: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)


@pytest.fixture(scope="function")
def db():
    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    # Recreate all tables
    Base.metadata.create_all(bind=engine)

    test_db = TestingSessionLocal()
    try:
        yield test_db
    finally:
        test_db.close()


def test_create_user(db):  # Add 'db' as an argument
    response = client.post("/users/Signup/", json={
        "user_id": 1,
        "name": "Anurag",
        "email": "abcd306@gmail.com",
        "password": "hellocoders",
        "time": "2022-01-01T00:00:00Z",
        "is_admin": False})
    db.delete(response.json)
    assert response.status_code == 201
    assert response.json() == {"message": "User created successfully"}


def test_get_all_users(db):  # Add 'db' as an argument

    response = client.get("/users/getallusers/",cookies={"token":""})
    data = response.json()
    assert response.status_code == 200
    assert data == [{"name": "Anurag",
                    "user_id": 1,
                     "email": "abcde123@gmail.com",
                     "is_admin": False}]
