from fastapi import APIRouter, Request, Response, status
from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from settings import database
from models import models, schemas
from utils import jwt_token, hash
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from handlers.authhandler import (
    LOGIN_USER,
    LOGOUT,
    FORGOT_PASSWORD,
    RESET_PASSWORD
)

from uuid import uuid1


router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user_login = LOGIN_USER(request, db)
    return user_login

#  Logout


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(res: Response):

    logout_user = LOGOUT(res)
    return logout_user


# forgot-password


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(request: schemas.ForgotPassword, db: Session = Depends(database.get_db)):

    reset_token = FORGOT_PASSWORD(request, db)
    return reset_token

# reset-password


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(reset_token: str, new_pass: str, db: Session = Depends(database.get_db)):

    reset = RESET_PASSWORD(reset_token, new_pass, db)
    return reset
