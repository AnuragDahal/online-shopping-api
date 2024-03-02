from fastapi import Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from settings import database
from models import models, schemas
from utils import jwt_token, hash
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from jose import jwt
from uuid import uuid1
from utils.exceptions import ErrorHandler
from utils.hash import Encryption
from settings.env_utils import Environment

env = Environment()

secret_key = env.secret_key
ALGORITHM = env.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = env.ACCESS_TOKEN_EXPIRE_MINUTES
TOKEN_TYPE = env.TOKEN_TYPE
TOKEN_KEY = env.TOKEN_KEY





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
        ErrorHandler.Error(e)


def validate_user(email: str, password: str, session: Session):
    user = session.query(models.User).filter(
        models.User.email == email).first()
    if user and Encryption.check_pw(user.password, password):
        return user


def LOGIN_USER(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = validate_user(request.username, request.password, db)
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
    return ErrorHandler.Unauthorized("Invalid email or password")


def LOGOUT(res: Response):
    try:
        res.delete_cookie(TOKEN_KEY)
        return {"message": "Logged out"}
    except Exception as e:
        ErrorHandler.Forbidden("Unable to logout user")


def FORGOT_PASSWORD(request: schemas.ForgotPassword, db: Session = Depends(database.get_db)):
    """[summary] verify the email and send the reset token to the email
    sending email is not implemented yet
    """
    email = request.email
    is_user = validate_email(email, db)
    if not is_user:
        ErrorHandler.Unauthorized("User with this Email not found")
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


def RESET_PASSWORD(reset_token: str, new_pass: str, db: Session = Depends(database.get_db)):
    """[summary] reset the password with the reset token
    """
    try:
        reset_token = db.query(models.ResetTokens).filter(
            models.ResetTokens.token == reset_token).first()
        if not reset_token:
            raise HTTPException(status_code=404, detail="Invalid reset token")
        email = reset_token.email

        # change the old password to new password
        CHANGE_PASSWORD(email, new_pass, db)

        # delete the reset token after the password is reset
        db.delete(reset_token)
        db.commit()

        return {"message": "Password reset successfully"}

    except Exception as e:
        ErrorHandler.Error(e)


def CHANGE_PASSWORD(email: str, new_pass: str, db: Session = Depends(database.get_db)):

    user_details = db.query(models.User).filter(
        models.User.email == email).first()
    user_details.password = hash.Encryption.bcrypt(new_pass)
    db.add(user_details)
    db.commit()
    db.refresh(user_details)
