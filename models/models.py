from sqlalchemy import Integer, String, Boolean, ForeignKey, DATETIME
from sqlalchemy.orm import relationship, Mapped, mapped_column
from settings.database import Base
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import List


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String)
    time: Mapped[str] = mapped_column(DATETIME, default=datetime.utcnow)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    # Define a one-to-many relationship to Order
    orders = relationship("Order", back_populates="users")


class Order(Base):
    __tablename__ = 'orders'

    order_id: Mapped[int] = mapped_column(
        Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'))
    status: Mapped[str] = mapped_column(String, default="pending")
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    # Define a many-to-one relationship to User and one to many relationship to Products
    users = relationship("User", back_populates="orders")
    product = relationship("Products", back_populates="orders")


class ResetTokens(Base):

    __tablename__ = 'ResetTokens'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[EmailStr] = mapped_column(String, nullable=False)
    token: Mapped[str] = mapped_column(String)


class Products(Base):
    __tablename__ = 'products'

    # here order_id and product_id are composite primary keys cause one order can have multiple products and one product can be in multiple orders
    order_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('orders.order_id'), primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String)
    # image: Mapped[str] = mapped_column(String)
    quantity: Mapped[int] = mapped_column(Integer)
    time: Mapped[str] = mapped_column(DATETIME, default=datetime.utcnow)
    orders = relationship("Order", back_populates="product")
