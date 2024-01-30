from fastapi import APIRouter, Depends, HTTPException, status
from config import database, models, schemas
from sqlalchemy.orm import Session
from .import users, oauth
from typing import List


router = APIRouter(
    tags=["Orders"]
)


@router.post("/CreateOrder", status_code=status.HTTP_201_CREATED)
async def create_order(request: schemas.Order, db: Session = Depends(database.get_db), current_user: schemas.UserLogin = Depends(oauth.get_current_user)):
    check_user = db.query(models.User).filter(
        models.User.user_id == request.user_id).first()
    if not check_user:
        raise HTTPException(
            status_code=404, detail="User not found please signup first")
    new_order = models.Order(
        user_id=request.user_id, product_name=request.product_name, product_id=request.product_id, quantity=request.quantity, total=request.total)
    if not new_order:
        raise HTTPException(status_code=400, detail="Invalid order data")
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return {"message": "Your Order has been placed  successfully"}


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
