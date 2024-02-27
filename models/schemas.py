from pydantic import BaseModel
from typing import Optional


class UserSignup(BaseModel):
    user_id: int
    name: str
    email: str
    password: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True


class Order(BaseModel):
    order_id: int
    user_id: int
    product_id: int
    quantity: int
    total: int

    class Config:
        from_attributes = True


class ShowAllUser(BaseModel):
    name: str
    user_id: int
    email: str
    is_admin: bool

    class Config:
        from_attributes = True


class OrderStatus(BaseModel):
    order_id: int
    product_id: int
    user_id: int
    status: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class ShowParticularUser(BaseModel):
    user_id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class ForgotPassword(BaseModel):
    email: str


# class UserOrders(BaseModel):
#     order_id: int
#     user_id: int
#     product_id: int
#     quantity: int
#     product_name: str
#     total: float

#     class Config:
#         from_attributes = True


# class ShowAllOrders(BaseModel):
#     order_id: int
#     user_id: int
#     product_id: int
#     quantity: int
#     product_name: str
#     total: float

#     class Config:
#         from_attributes = True
