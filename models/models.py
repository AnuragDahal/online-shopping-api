from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DATETIME
from sqlalchemy.orm import relationship, Mapped
from ..settings.database import Base
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String)
    email: Mapped[str] = Column(String, nullable=False)
    password: Mapped[str] = Column(String)
    time: Mapped[str] = Column(DATETIME, default=datetime.utcnow)
    is_admin: Mapped[bool] = Column(Boolean, default=False)

    # Define a one-to-many relationship to Order
    orders = relationship("Order", back_populates="users")


class Order(Base):
    __tablename__ = 'orders'

    order_id: Mapped[int] = Column(
        Integer, primary_key=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey('users.user_id'))
    product_id: Mapped[int] = Column(Integer)
    total: Mapped[int] = Column(Integer)
    status: Mapped[str] = Column(String, default="pending")
    quantity: Mapped[int] = Column(Integer, default=1)
    # Define a many-to-one relationship to User
    users = relationship("User", back_populates="orders")


class ResetTokens(Base):

    __tablename__ = 'ResetTokens'

    id: Mapped[int] = Column(Integer, primary_key=True)
    email: Mapped[EmailStr] = Column(String, nullable=False)
    token: Mapped[str] = Column(String)
