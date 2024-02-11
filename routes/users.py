from fastapi import APIRouter, HTTPException, status, Depends, Request
from settings import database
from sqlalchemy.orm import Session
from typing import List

from models import models, schemas
from utils import hash
from utils.jwt_token import verify_token
router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


def is_user(user_id: int, db: Session = Depends(database.get_db)):
    try:
        user = db.query(models.User).filter(
            models.User.user_id == user_id).first()
        if user:
            return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e))


@router.post("/Signup", status_code=status.HTTP_201_CREATED)
async def create_user(request: schemas.UserSignup, db: Session = Depends(database.get_db)):

    # Check if the email already exists
    if db.query(models.User).filter(models.User.email == request.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    hashed_password = hash.Encryption.bcrypt(request.password)
    # Create a new user
    new_user = models.User(
        name=request.name, email=request.email, password=hashed_password)

    # Add the new user to the database
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}


@router.get("/getallusers", response_model=List[schemas.ShowAllUser], status_code=status.HTTP_200_OK)
async def get_all_users(db: Session = Depends(database.get_db), dependencies: Session = Depends(verify_token)):
    user = db.query(models.User).all()
    if not user:
        raise HTTPException(status_code=404, detail="No users found")
    return user

# know the user_details [ for all users]


@router.get("/getuser/{email}", response_model=schemas.ShowParticularUser, status_code=status.HTTP_200_OK)
async def get_user(email: str, db: Session = Depends(database.get_db), dependencies: Session = Depends(verify_token)):
    user = db.query(models.User).filter(
        models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# get user details with user id


@router.get("/getuserbyid/{user_id}", response_model=schemas.ShowParticularUser, status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int, db: Session = Depends(database.get_db), dependencies: Session = Depends(verify_token)):
    user = db.query(models.User).filter(
        models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
