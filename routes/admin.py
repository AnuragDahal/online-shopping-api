from fastapi import HTTPException, Depends, status
from fastapi import APIRouter, Depends, HTTPException, status
from config import database, models, schemas
from sqlalchemy.orm import Session
from . import oauth, users, auth
from typing import List

router = APIRouter(
    tags=["Admin"]
)

# Update user to admin


@router.put("/update-to-admin/{user_id}", status_code=status.HTTP_200_OK)
async def UPDATEADMIN(user_id: int, admin_id: int, db: Session = Depends(database.get_db)):
    try:
        admin_data = auth.check_isadmin(admin_id, db)
        user_data = users.is_user(user_id, db)
        if admin_data and user_data:
            user_update = db.query(models.User).filter(
                models.User.user_id == user_id).first()
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f"{e}, Error updating user to admin")


@router.get("/get-allorders/{admin_id}",  status_code=status.HTTP_200_OK)
async def get_all_orders(admin_id: int, db: Session = Depends(database.get_db), current_user: schemas.UserLogin = Depends(oauth.get_current_user)):
    user_data = users.is_user(admin_id, db)
    if not user_data:
        return {"message": "Invalid admin/user id please signup first and login as admin"}
    admin_data = auth.check_isadmin(admin_id, db)
    if admin_data:
        orders = db.query(models.Order).all()
        if not orders:
            raise HTTPException(
                status_code=404, detail="No orders has been placed yet")
        return orders
    return {"message": "You are not an admin"}


# update order status by admin


@router.put("/order/update/status/{order_id}", response_model=schemas.OrderStatus, status_code=status.HTTP_200_OK)
async def update_order_status(order_id: int, admin_id: int, request: schemas.OrderStatus, db: Session = Depends(database.get_db), current_user: schemas.UserLogin = Depends(oauth.get_current_user)):
    # user_data = users.is_user(admin_id, db)
    # if not user_data:
    #     return {"message": "Invalid admin id please signup first and login as admin"}
    admin_data = auth.check_isadmin(admin_id, db)
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

# get orders by status [admin]
# status_list = ["pending", "delivered", "cancelled"]


@router.get("/getorders-bystatus/{status}", response_model=List[schemas.Order], status_code=status.HTTP_200_OK)
async def get_orders_by_status(status: str, db: Session = Depends(database.get_db), current_user: schemas.UserLogin = Depends(oauth.get_current_user)):
    orders = db.query(models.Order).filter(models.Order.status == status).all()
    if not orders:
        raise HTTPException(
            status_code=404, detail=f"No orders found of {status} status")
    return orders
