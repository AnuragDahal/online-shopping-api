from fastapi import APIRouter, Depends, status, Depends
from settings import database
from sqlalchemy.orm import Session
from models import schemas
from utils.jwt_token import verify_token
from typing import List
from starlette.requests import Request
from handlers.orderhandler import (
    CREATE_ORDER,
    CANCEL_ORDER,
    GET_USER_ORDERS,
    GET_ORDER_STATUS,
    GET_ORDERS_BY_ID,
)


router = APIRouter(
    tags=["Orders"],
    dependencies=[Depends(verify_token)],
)


@router.post("/createorder", status_code=status.HTTP_201_CREATED)
async def create_order(req: schemas.Order, db: Session = Depends(database.get_db)):

    new_order = CREATE_ORDER(req, db)
    return [new_order]

# cancel order


@router.delete("/cancel-order/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_order(order_id: int, request: Request, db: Session = Depends(database.get_db)):

    cancelled_order = CANCEL_ORDER(order_id, request, db)
    return cancelled_order


@router.get("/user/order/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_orders(
    user_id: int, request: Request, db: Session = Depends(database.get_db)
):

    orders = GET_USER_ORDERS(user_id, request, db)
    return orders


# get status of a particular order
@router.get("/order/status/{order_id}", response_model=schemas.OrderStatus, status_code=status.HTTP_200_OK)
async def get_order_status(order_id: int, db: Session = Depends(database.get_db)):

    order_status = GET_ORDER_STATUS(order_id, db)
    return order_status


@router.get("/users/orders/{order_id}", response_model=List[schemas.Order], status_code=status.HTTP_200_OK)
async def get_orders_by_id(order_id: int, db: Session = Depends(database.get_db)):

    orders = GET_ORDERS_BY_ID(order_id, db)
    return orders
