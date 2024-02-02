from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from .database import Base


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String)
    email: Mapped[str] = Column(String, nullable=False)
    password: Mapped[str] = Column(String)
    time: Mapped[str] = Column(String)
    is_admin: Mapped[bool] = Column(Boolean, default=False)

    # Define a one-to-many relationship to Order
    orders = relationship("Order", back_populates="users")


class Order(Base):
    __tablename__ = 'orders'

    order_id: Mapped[int] = Column(Integer, primary_key=True,)
    user_id: Mapped[int] = Column(Integer, ForeignKey('users.user_id'))
    product_id: Mapped[int] = Column(Integer)
    total: Mapped[int] = Column(Integer)
    status: Mapped[str] = Column(String, default="pending")

    # Define a many-to-one relationship to User
    users = relationship("User", back_populates="orders")
