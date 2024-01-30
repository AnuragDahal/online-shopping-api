from fastapi import APIRouter, HTTPException, status, Depends
from config import database, models, schemas
from sqlalchemy.orm import Session
from typing import List
from . import oauth

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/Signup", status_code=status.HTTP_201_CREATED)
async def create_user(request: schemas.UserSignup, db: Session = Depends(database.get_db)):

    # Check if the email already exists
    if db.query(models.User).filter(models.User.email == request.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    # Create a new user
    new_user = models.User(
        name=request.name, email=request.email, password=request.password)

    # Add the new user to the database
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}


# @router.post("/login", status_code=status.HTTP_200_OK)
# async def login_user(request: schemas.UserLogin, db: Session = Depends(database.get_db)):

#     user = db.query(models.User).filter(
#         models.User.email == request.email).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     if not user.password == request.password:
#         raise HTTPException(status_code=404, detail="Incorrect password")
#     return {"message": "User logged in successfully"}

@router.get("/GetAllUsers", response_model=List[schemas.ShowAllUser], status_code=status.HTTP_200_OK)
async def get_all_users(db: Session = Depends(database.get_db), current_user: schemas.UserLogin = Depends(oauth.get_current_user)):
    user = db.query(models.User).all()
    if not user:
        raise HTTPException(status_code=404, detail="No users found")
    return user
# u


def check_isadmin(admin_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.user_id == admin_id).first()
    if user and user.is_admin == True:
        return True
    return False


def is_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user:
        return True
    return False
