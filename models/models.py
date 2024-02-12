from sqlalchemy import mapped_column, Integer, String, Boolean, ForeignKey, DATETIME
from sqlalchemy.orm import relationship, Mapped , mapped_column
from settings.database import Base
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr



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
    product_id: Mapped[int] = mapped_column(Integer)
    total: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String, default="pending")
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    # Define a many-to-one relationship to User
    users = relationship("User", back_populates="orders")


class ResetTokens(Base):

    __tablename__ = 'ResetTokens'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[EmailStr] = mapped_column(String, nullable=False)
    token: Mapped[str] = mapped_column(String)
