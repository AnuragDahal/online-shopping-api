from fastapi import HTTPException, Depends, status
from settings import database
from models import schemas, models
from utils import oauth
from sqlalchemy.orm import Session
from routes import users
from utils.exceptions import ErrorHandler


def check_isadmin(admin_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.user_id == admin_id).first()
    if user and user.is_admin == True:
        return True
    return False


def UPDATE_ADMIN(user_id: int, admin_id: int, db: Session = Depends(database.get_db)):
    try:
        admin_data = check_isadmin(admin_id, db)
        user_data = users.is_user(user_id, db)

        if admin_data and user_data:
            user_update = db.query(models.User).filter(
                models.User.user_id == user_id).first()
            user_update.is_admin = True
            db.add(user_update)
            db.commit()
            db.refresh(user_update)
            return {"message": "User has been updated to admin"}
    except Exception as e:
        ErrorHandler.Unauthorized(e)


def GET_ALL_ORDERS(admin_id: int, db: Session = Depends(database.get_db)):
    user_data = users.is_user(admin_id, db)
    if not user_data:
        return {"message": "Invalid admin/user id please signup first and login as admin"}
    admin_data = check_isadmin(admin_id, db)
    if admin_data:
        orders = db.query(models.Order).all()
        if not orders:
            ErrorHandler.NotFound("No orders found")
    ErrorHandler.Unauthorized("You are not an admin")


def UPDATE_ORDER_STATUS(order_id: int, admin_id: int, request: schemas.OrderStatus, db: Session = Depends(database.get_db)) -> schemas.OrderStatus:

    admin_data = check_isadmin(admin_id, db)
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
    ErrorHandler.Unauthorized("You are not an admin")


def GET_ORDERS_BY_STATUS(status: str, db: Session = Depends(database.get_db)):
    try:
        if status not in ["pending", "delivered", "cancelled"]:
            ErrorHandler.NotFound(
                "Invalid status, status can be either pending, delivered or cancelled")
        orders = db.query(models.Order).filter(
            models.Order.status == status).all()
        if not orders:
            return {"message": "No orders found"}
        return orders
    except Exception as e:
        ErrorHandler.Error(e)
