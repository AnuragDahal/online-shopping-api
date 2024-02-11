from fastapi import APIRouter, Request, Response, status
from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from  settings import database
from models import models, schemas
from utils import jwt_token,hash
from datetime import timedelta
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from utils.jwt_token import verify_token
from jose import JWTError, jwt
from uuid import uuid1

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


def UserHandler(request: Request, session: Session = Depends(database.get_db)) -> models.User:
    cookie_token = request.cookies.get("token")
    payload = jwt.decode(cookie_token, secret_key, algorithms=[ALGORITHM])
    email: str = payload.get("sub")
    user = validate_email(email, session)
    if user:
        return user


def validate_email(email: str, session: Session):
    try:
        user = session.query(models.User).filter(
            models.User.email == email).first()
        if user:
            return user
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f"{e}, validate_email error")


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

# forgot-password


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(request: schemas.ForgotPassword, db: Session = Depends(database.get_db)):

    """[summary] verify the email and send the reset token to the email
    sending email is not implemented yet
    """
    email = request.email
    is_user = validate_email(email, db)
    if not is_user:
        raise HTTPException(
            status_code=404, detail="User with the email not found")
    reset_token = str(uuid1())
    set_token = {
        "email": email,
        "token": reset_token,
    }
    set_reset_token = models.ResetTokens(**set_token)
    db.add(set_reset_token)
    db.commit()
    db.refresh(set_reset_token)
    return reset_token

# reset-password


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(reset_token: str, new_pass: str, db: Session = Depends(database.get_db)):
    """[summary] reset the password with the reset token
    """
    try:
        reset_token = db.query(models.ResetTokens).filter(
            models.ResetTokens.token == reset_token).first()
        if not reset_token:
            raise HTTPException(status_code=404, detail="Invalid reset token")
        email = reset_token.email

        # change the old password to new password
        change_password(email, new_pass, db)

        # delete the reset token after the password is reset
        db.delete(reset_token)
        db.commit()

        return {"message": "Password reset successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def change_password(email: str, new_pass: str, db: Session = Depends(database.get_db)):

    user_details = db.query(models.User).filter(
        models.User.email == email).first()
    user_details.password = hash.Encryption.bcrypt(new_pass)
    db.add(user_details)
    db.commit()
    db.refresh(user_details)
