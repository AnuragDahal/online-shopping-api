from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from settings import database
from models import models, schemas
from handlers.authhandler import UserHandler
from utils.exceptions import ErrorHandler
from sqlalchemy.orm import joinedload


def CREATE_ORDER(req: schemas.Order, db: Session = Depends(database.get_db)):
    new_order = models.Order(**req.model_dump(exclude={"product"}))
    for items in req.product:
        product_data = models.Products(
            **items.model_dump(exclude={"order_id"}), order_id=new_order.order_id)
        db.add(product_data)
        db.commit()
    db.add(new_order)
    db.commit()
    return req


def CANCEL_ORDER(order_id: int, request: Request, db: Session = Depends(database.get_db)):
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
    return {"message": "Order and associated products have been cancelled"}


def GET_USER_ORDERS(user_id: int, request: Request, db: Session = Depends(database.get_db)):
    current_user = UserHandler(request, db)
    if current_user.user_id == user_id:
        orders = db.query(models.Order).filter(
            models.Order.user_id == user_id).all()
        return orders
    ErrorHandler.Forbidden("You are not authorized to view this order")


def GET_ORDERS_BY_ID(order_id: int, db: Session):
    order = db.query(models.Order).options(joinedload(models.Order.products)).filter(
        models.Order.order_id == order_id).first()

    if order is None:
        ErrorHandler.NotFound("Order not found")

    order_columns = order.__table__.columns
    order_dict = {c.name: getattr(order, c.name) for c in order_columns}

    if order.products:
        product_columns = order.products[0].__table__.columns
        order_dict["product"] = [{c.name: getattr(
            product, c.name) for c in product_columns} for product in order.products]

    return [order_dict]


def GET_ORDER_STATUS(order_id: int, db: Session = Depends(database.get_db)):
    order = db.query(models.Order).filter(
        models.Order.order_id == order_id).first()
    if not order:
        ErrorHandler.NotFound("Order not found")
    return order
