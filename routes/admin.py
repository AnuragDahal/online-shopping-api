from fastapi import APIRouter, Depends, Request, status
from settings import database
from sqlalchemy.orm import Session
from handlers.authhandler import verify_admin
from handlers.adminhandler import (
    UPDATE_ADMIN,
    GET_ALL_ORDERS,
    UPDATE_ORDER_STATUS,
    GET_ORDERS_BY_STATUS)
from models import schemas
from utils import oauth
from typing import List

router = APIRouter(
    tags=["Admin"],
    # dependencies=[Depends(oauth.get_current_user)]
)

# Update user to admin


@router.put("/update-to-admin/{user_id}", status_code=status.HTTP_200_OK)
async def update_to_admin(user_id: int, admin: bool = Depends(verify_admin), db: Session = Depends(database.get_db)):
    updated_user = UPDATE_ADMIN(user_id, db)
    return updated_user


@router.get("/get-allorders",  status_code=status.HTTP_200_OK)
async def all_orders(admin: bool = Depends(verify_admin), db: Session = Depends(database.get_db)):

    orders = GET_ALL_ORDERS(db)
    return orders

# update order status by admin


@router.put("/order/update/status/{order_id}", response_model=List[schemas.OrderStatus], status_code=status.HTTP_200_OK)
async def update_order_status(order_id: int, status: str, admin: bool = Depends(verify_admin), db: Session = Depends(database.get_db)):

    status = UPDATE_ORDER_STATUS(order_id, status, db)
    return status


@router.get("/getorders-bystatus", response_model=List[schemas.OrderStatus], status_code=status.HTTP_200_OK)
async def get_orders_by_status(status: str, admin: bool = Depends(verify_admin), db: Session = Depends(database.get_db)):

    orders_by_status = GET_ORDERS_BY_STATUS(status, db)
    return orders_by_status
