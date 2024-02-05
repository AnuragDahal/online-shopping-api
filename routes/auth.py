from fastapi import APIRouter, Request, Response, status
from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from config import models, database, schemas
from . import hash, jwt_token
from datetime import timedelta
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from .jwt_token import verify_token
from jose import JWTError, jwt

import os

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.environ.get("Access_Token_Expire_Minutes"))
secret_key = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


router = APIRouter(
    tags=["Authentication"]
)

INVALID_CREDENTIALS = "Invalid Credentials"
TOKEN_TYPE = "bearer"
TOKEN_KEY = "token"


def UserHandler(request: Request, dependencies: Session = Depends(verify_token), db: Session = Depends(database.get_db)):
    try:
        cookie_token = request.cookies.get("token")
        payload = jwt.decode(cookie_token, secret_key, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        user = validate_email(email, db)

        if user:
            print(user)
            return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def validate_email(email: str, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")
    return user


def check_isadmin(admin_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.user_id == admin_id).first()
    if user and user.is_admin == True:
        return True
    return False


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = validate_email(request.username, db)
    if user:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = jwt_token.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )

        response = JSONResponse(
            content={"access_token": access_token, "token_type": TOKEN_TYPE}
        )

        response.set_cookie(key=TOKEN_KEY, value=access_token,
                            expires=access_token_expires.total_seconds())

        return response
    return {"message": "Invalid credentials"}

#  Logout


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(res: Response):
    try:
        res.delete_cookie(TOKEN_KEY)
        return {"message": "Logged out"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
