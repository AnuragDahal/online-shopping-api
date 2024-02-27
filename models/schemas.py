from pydantic import BaseModel
from typing import Optional, List


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


class Product(BaseModel):
    order_id: int
    product_id: int
    name: Optional[str]
    quantity: int
    price: int
    total: int

    class Config:
        from_attributes = True


class Order(BaseModel):
    order_id: int
    user_id: int
    product: List[Product]

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
