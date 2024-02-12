from fastapi import HTTPException, Depends, status
from fastapi import APIRouter, Depends, HTTPException, status
from settings import database
from sqlalchemy.orm import Session
from handlers.adminhandler import (
    UPDATE_ADMIN, GET_ALL_ORDERS, UPDATE_ORDER_STATUS, GET_ORDERS_BY_STATUS)
from models import schemas
from utils import oauth
from typing import List

router = APIRouter(
    tags=["Admin"]
)

# Update user to admin


@router.put("/update-to-admin/{user_id}", status_code=status.HTTP_200_OK)
async def update_to_admin(user_id: int, admin_id: int, current_user: schemas.UserLogin = Depends(oauth.get_current_user), db: Session = Depends(database.get_db)):

    updated_user = UPDATE_ADMIN(
        user_id=user_id, admin_id=admin_id, current_user=current_user, db=db)
    return updated_user


@router.get("/get-allorders/{admin_id}",  status_code=status.HTTP_200_OK)
async def all_orders(admin_id: int, db: Session = Depends(database.get_db), current_user: schemas.UserLogin = Depends(oauth.get_current_user)):

    orders = GET_ALL_ORDERS(admin_id, db)
    return orders

# update order status by admin


@router.put("/order/update/status/{order_id}", response_model=List[schemas.OrderStatus], status_code=status.HTTP_200_OK)
async def update_order_status(order_id: int, admin_id: int, request: schemas.OrderStatus, db: Session = Depends(database.get_db), current_user: schemas.UserLogin = Depends(oauth.get_current_user)):

    status = UPDATE_ORDER_STATUS(order_id, admin_id, request, db)
    return status


@router.get("/getorders-bystatus", status_code=status.HTTP_200_OK)
async def get_orders_by_status(status: str, db: Session = Depends(database.get_db), current_user: schemas.UserLogin = Depends(oauth.get_current_user)):

    orders_by_status = GET_ORDERS_BY_STATUS(status, db)
    return schemas.OrderStatus(orders_by_status)
