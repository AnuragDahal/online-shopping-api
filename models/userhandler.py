from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from models import models, schemas
from settings import database
from utils import hash
from utils.jwt_token import verify_token
from utils.exceptions import ErrorHandler
import logging


def IS_USER(user_id: int, db: Session = Depends(database.get_db)):
    try:
        user = db.query(models.User).filter(
            models.User.user_id == user_id).first()
        if user:
            return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e))


def CREATE_USER(request: schemas.UserSignup, db: Session = Depends(database.get_db)):

    # Check if the email already exists
    if db.query(models.User).filter(models.User.email == request.email).first():
        ErrorHandler.Conflict("Email already exists")
    hashed_password = hash.Encryption.bcrypt(request.password)
    # Create a new user
    new_user = models.User(
        **request.model_dump(exclude={"password"}), password=hashed_password)
    # Add the new user to the database
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}


def GET_ALL_USERS(db: Session = Depends(database.get_db), dependencies: Session = Depends(verify_token)):
    user = db.query(models.User).all()
    if not user:
        ErrorHandler.NotFound("No user found")
    return user


def GET_USER(email: str, db: Session = Depends(database.get_db), dependencies: Session = Depends(verify_token)):
    user = db.query(models.User).filter(
        models.User.email == email).first()
    if not user:
        ErrorHandler.NotFound("User not found")
    return user


def GET_USER_BY_ID(user_id: int, db: Session = Depends(database.get_db), dependencies: Session = Depends(verify_token)):
    user = db.query(models.User).filter(
        models.User.user_id == user_id).first()
    if not user:
        ErrorHandler.NotFound("User not found")
    return user
