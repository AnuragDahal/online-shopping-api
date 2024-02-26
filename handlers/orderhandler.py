from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from settings import database
from models import models, schemas
from handlers.authhandler import UserHandler
from utils.exceptions import ErrorHandler


def CREATE_ORDER(req: schemas.Order, db: Session = Depends(database.get_db)):
    try:
        new_order = models.Order(**req.model_dump(exclude=None))

        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return new_order
    except Exception as e:
        ErrorHandler.Error(e)


def CANCEL_ORDER(order_id: int, request: Request, db: Session = Depends(database.get_db)):
    try:
        curr_user = UserHandler(request, db)
        user_order = db.query(models.Order).filter(
            models.Order.user_id == curr_user.user_id).all()
        if order_id not in [order.order_id for order in user_order]:
            ErrorHandler.Forbidden(
                "You are not authorized to cancel this order")
        cancel_order = db.query(models.Order).filter(
            models.Order.order_id == order_id).first()
        db.delete(cancel_order)
        db.commit()
        return {"message": "Order has been cancelled"}
    except Exception as e:
        ErrorHandler.Error(e)


def GET_USER_ORDERS(user_id: int, request: Request, db: Session = Depends(database.get_db)):
    try:
        current_user = UserHandler(request, db)
        if current_user.user_id == user_id:
            orders = db.query(models.Order).filter(
                models.Order.user_id == user_id).all()
            return orders
    except Exception as e:
        ErrorHandler.NotFound(e)


def GET_ORDER_STATUS(order_id: int, db: Session = Depends(database.get_db)):
    order = db.query(models.Order).filter(
        models.Order.order_id == order_id).first()
    if not order:
        ErrorHandler.NotFound("Order not found")
    return order
