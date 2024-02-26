from fastapi import APIRouter, HTTPException, status, Depends
from settings.database import db_dependency
from sqlalchemy.orm import Session
from typing import List
from models import schemas
from utils.jwt_token import verify_token
from handlers.userhandler import (
    CREATE_USER,
    GET_ALL_USERS,
    GET_USER,
    GET_USER_BY_ID

)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/Signup", status_code=status.HTTP_201_CREATED)
async def create_user(request: schemas.UserSignup, db: db_dependency):
    new_user = CREATE_USER(request, db)
    return new_user


@router.get("/getallusers", response_model=List[schemas.ShowAllUser], status_code=status.HTTP_200_OK)
async def get_all_users(db: db_dependency, dependencies: Session = Depends(verify_token)):

    user = GET_ALL_USERS(db)
    return user

# get user details with email


@router.get("/getuser/{email}", response_model=schemas.ShowParticularUser, status_code=status.HTTP_200_OK)
async def get_user(email: str, db: db_dependency, dependencies: Session = Depends(verify_token)):

    user_details = GET_USER(email, db)
    return user_details

# get user details with user id


@router.get("/getuserbyid/{user_id}", response_model=schemas.ShowParticularUser, status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int, db: db_dependency, dependencies: Session = Depends(verify_token)):

    user_by_id = GET_USER_BY_ID(user_id, db)
    return user_by_id
