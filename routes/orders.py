from fastapi import APIRouter, Depends, HTTPException, status
from config import database, models, schemas
from sqlalchemy.orm import Session
from .import users, oauth, auth
from typing import List


router = APIRouter(
    tags=["Orders"]
)


@router.post("/CreateOrder", status_code=status.HTTP_201_CREATED)
async def create_order(request: schemas.Order, db: Session = Depends(database.get_db), current_user: schemas.UserLogin = Depends(oauth.get_current_user)):
    user = users.is_user(request.user_id, db)
    if user:
        new_order = models.Order(

        )
        if not new_order:
            raise HTTPException(status_code=400, detail="Invalid order data")

        db.add(new_order)
        db.commit()
        return {"message": "Order has been placed successfully"}
    return {"message": "Invalid user id please signup first"}

# get all orders of a particular user


@router.get("/user/order/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_orders(user_id: int, db: Session = Depends(database.get_db), current_user: schemas.UserLogin = Depends(oauth.get_current_user)):
    user_data = users.is_user(user_id, db)
    if not user_data:
        return {"message": "Invalid user id please signup first"}
    orders = db.query(models.Order).filter(
        models.Order.user_id == user_id).all()
    if not orders:
        raise HTTPException(
            status_code=404, detail="NO orders has been placed yet")
    return orders


# get status of a particular order
@router.get("/order/status/{order_id}", response_model=schemas.OrderStatus, status_code=status.HTTP_200_OK)
async def get_order_status(order_id: int, db: Session = Depends(database.get_db), current_user: schemas.UserLogin = Depends(oauth.get_current_user)):
    order = db.query(models.Order).filter(
        models.Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
