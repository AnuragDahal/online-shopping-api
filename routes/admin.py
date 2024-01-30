from fastapi import APIRouter, Depends, HTTPException, status
from config import database, models, schemas
from sqlalchemy.orm import Session
from . import oauth, users
from typing import List

router = APIRouter(
    tags=["Admin"]
)

# Update user to admin


@router.put("/update-user/{admin_id}", status_code=status.HTTP_202_ACCEPTED, tags=["Admin"])
async def update_user_to_admin(admin_id: int, user_id: int, db: Session = Depends(database.get_db), current_user: schemas.UserLogin = Depends(oauth.get_current_user)):
    admin_data = db.query(models.User).filter(
        models.User.user_id == admin_id).first()
    if admin_data and admin_data.is_admin:
        user_data = db.query(models.User).filter(
            models.User.user_id == user_id).first()
        if user_data:
            user_data.is_admin = True
            db.add(user_data)
            db.commit()
            return {"message": "User updated to admin successfully"}
        else:
            return {"message": "User not found"}
    return {"message": "You are not admin"}


# get all orders only by admin


@router.get("/get-allorders/{admin_id}",  status_code=status.HTTP_200_OK)
async def get_all_orders(admin_id: int, db: Session = Depends(database.get_db), current_user: schemas.UserLogin = Depends(oauth.get_current_user)):
    user_data = users.is_user(admin_id, db)
    if not user_data:
        return {"message": "Invalid admin/user id please signup first and login as admin"}
    admin_data = users.check_isadmin(admin_id, db)
    if admin_data:
        orders = db.query(models.Order).all()
        if not orders:
            raise HTTPException(
                status_code=404, detail="No orders has been placed yet")
        return orders
    return {"message": "You are not an admin"}


# uodate order status by admin


@router.put("/order/update/status/{order_id}", response_model=schemas.OrderStatus, status_code=status.HTTP_200_OK)
async def update_order_status(order_id: int, admin_id: int, request: schemas.OrderStatus, db: Session = Depends(database.get_db), current_user: schemas.UserLogin = Depends(oauth.get_current_user)):
    # user_data = users.is_user(admin_id, db)
    # if not user_data:
    #     return {"message": "Invalid admin id please signup first and login as admin"}
    admin_data = users.check_isadmin(admin_id, db)
    if admin_data:
        order = db.query(models.Order).filter(
            models.Order.order_id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        order.status = request.status
        db.add(order)
        db.commit()
        db.refresh(order)
        return order
    return {"message": "You are not an admin"}
