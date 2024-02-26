from fastapi import HTTPException, Request
from settings.database import db_dependency
from models import models, schemas
from handlers.authhandler import UserHandler


def CREATE_ORDER(req: schemas.Order, db: db_dependency):
    try:
        new_order = models.Order(**req.model_dump(exclude={"product"}))
        for product in req.product:
            new_product = models.Products(
                **product.model_dump(exclude={"order_id"}))
            db.add(new_product)
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return new_order
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}, Order not created")


def CANCEL_ORDER(order_id: int, request: Request, db: db_dependency):
    try:
        curr_user = UserHandler(request, db)
        user_order = db.query(models.Order).filter(
            models.Order.user_id == curr_user.user_id).all()
        if order_id not in [order.order_id for order in user_order]:
            raise HTTPException(
                status_code=404, detail="Order not found, cannot cancel")
        cancel_order = db.query(models.Order).filter(
            models.Order.order_id == order_id).first()
        db.delete(cancel_order)
        db.commit()
        return {"message": "Order has been cancelled"}
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f"{e}, Error cancelling order")


def GET_USER_ORDERS(user_id: int, request: Request, db: db_dependency):
    try:
        current_user = UserHandler(request, db)
        if current_user.user_id == user_id:
            orders = db.query(models.Order).filter(
                models.Order.user_id == user_id).all()
            return orders
    except Exception as e:
        raise HTTPException(
            status_code=404, detail=f"{e}, Error fetching orders")


def GET_ORDER_STATUS(order_id: int, db: db_dependency):
    order = db.query(models.Order).filter(
        models.Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
