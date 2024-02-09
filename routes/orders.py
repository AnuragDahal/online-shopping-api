from fastapi import APIRouter, Depends, HTTPException, status, Depends, Response
from config import database, models, schemas
from sqlalchemy.orm import Session
from .import users, oauth, auth
from .jwt_token import verify_token
from typing import List
from starlette.requests import Request

router = APIRouter(
    tags=["Orders"],
    dependencies=[Depends(verify_token)],
)


@router.post("/createorder", status_code=status.HTTP_201_CREATED)
async def create_order(req: schemas.Order, db: Session = Depends(database.get_db)):
    try:
        new_order = models.Order(
            order_id=req.order_id,
            user_id=req.user_id,
            product_id=req.product_id,
            quantity=req.quantity,
            total=req.total
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return new_order
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}, Order not created")


# cancel order


@router.delete("/cancel-order/{order_id}", status_code=status.HTTP_200_OK)
async def cancel_order(order_id: int, request: Request, db: Session = Depends(database.get_db)):
    try:
        curr_user = auth.UserHandler(request, db)
        user_order = db.query(models.Order).filter(
            models.Order.user_id == curr_user.user_id).first()
        if user_order:
            cancel_order = db.query(models.Order).filter(
                models.Order.order_id == order_id).first()
            db.delete(cancel_order)
            db.commit()
            return {"message": "Order has been cancelled"}
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f"{e}, Error cancelling order")


@router.get("/user/order/{user_id}", response_model=List[schemas.Order], status_code=status.HTTP_200_OK)
async def get_user_orders(
    user_id: int,
    request: Request,
    db: Session = Depends(database.get_db),
):
    current_user = auth.UserHandler(request, db)
    print(current_user.user_id)
    if current_user.user_id == user_id:
        orders = db.query(models.Order).filter(
            models.Order.user_id == user_id).all()
        return orders
    else:
        raise HTTPException(
            status_code=404, detail="Error fetching orders")


# get status of a particular order
@router.get("/order/status/{order_id}", response_model=schemas.OrderStatus, status_code=status.HTTP_200_OK)
async def get_order_status(order_id: int, db: Session = Depends(database.get_db)):
    order = db.query(models.Order).filter(
        models.Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
