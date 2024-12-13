from fastapi import HTTPException, Depends
from settings import database
from models import schemas, models
from sqlalchemy.orm import Session
from utils.exceptions import ErrorHandler
from handlers import userhandler
from sqlalchemy.orm import joinedload


def UPDATE_ADMIN(user_id: int, db: Session = Depends(database.get_db)):
    try:            # check the validation of the user to be updated to admin
        user_data = userhandler.IS_USER(user_id, db)
        if user_data:
            user_update = db.query(models.User).filter(
                models.User.user_id == user_id).first()
            user_update.is_admin = True
            db.add(user_update)
            db.commit()
            db.refresh(user_update)
            return {"message": "User has been updated to admin"}
    except Exception as e:
        ErrorHandler.Unauthorized(e)


def GET_ALL_ORDERS(db: Session = Depends(database.get_db)):
    orders = db.query(models.Order).options(
        joinedload(models.Order.products)).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")

    orders_list = []
    for order in orders:
        order_dict = {c.name: getattr(order, c.name)
                      for c in order.__table__.columns}
        order_dict["product"] = [{c.name: getattr(
            product, c.name) for c in product.__table__.columns} for product in order.products]
        orders_list.append(order_dict)

    return orders_list


def UPDATE_ORDER_STATUS(order_id: int, status: str, db: Session = Depends(database.get_db)) -> schemas.OrderStatus:

    order = db.query(models.Order).filter(
        models.Order.order_id == order_id).first()
    if not order:
        ErrorHandler.NotFound("Order not found")
    order.status = status
    db.add(order)
    db.commit()
    db.refresh(order)
    return [order]


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
