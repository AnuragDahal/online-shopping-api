from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from config import models, database, schemas
from . import hash, jwt_token
from datetime import timedelta
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

import os

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.environ.get("Access_Token_Expire_Minutes"))


get_db = database.get_db


router = APIRouter(
    tags=["Authentication"]
)

INVALID_CREDENTIALS = "Invalid Credentials"
TOKEN_TYPE = "bearer"
TOKEN_KEY = "token"


async def validate_user(request: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter_by(email=request.email).first()

    if not user or not hash.Encryption.check_pw(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )
    return True


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = validate_user(db, request.username, request.password)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt_token.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    response = JSONResponse(
        content={"access_token": access_token, "token_type": TOKEN_TYPE}
    )
    response.set_cookie(key=TOKEN_KEY, value=access_token,
                        expires=access_token_expires.total_seconds(), httponly=True, secure=True)

    return response
