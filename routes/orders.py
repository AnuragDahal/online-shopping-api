from fastapi import APIRouter, Depends, HTTPException, status, Request, Depends, Response
from config import database, models, schemas
from sqlalchemy.orm import Session
from .import users, oauth, auth
from .jwt_token import verify_token
from typing import List

router = APIRouter(
    tags=["Orders"],
    dependencies=[Depends(verify_token)]
)


@router.post("/createorder", status_code=status.HTTP_201_CREATED)
async def create_order(req: schemas.Order, db: Session = Depends(database.get_db)):
    try:
        new_order = models.Order(
            order_id=req.order_id,
            user_id=req.user_id,
            product_id=req.product_id,
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return new_order
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}, Order not created")


# cancel order


@router.delete("/cancel-order/{order_id}", status_code=status.HTTP_200_OK)
async def cancel_order(order_id: int, db: Session = Depends(database.get_db)):
    try:
        order = db.query(models.Order).filter_by(
            models.Order.order_id == order_id).first()
        db.delete(order)
        db.commit()
        db.refresh(order)
        return {"message": "Order has been cancelled"}
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail="Order not found")


@router.get("/user/order/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_orders(user_id: int, db: Session = Depends(database.get_db)):
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
async def get_order_status(order_id: int, db: Session = Depends(database.get_db)):
    order = db.query(models.Order).filter(
        models.Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
