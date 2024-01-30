from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from config import schemas
import os

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
access_token_expires = os.environ.get("Access_Token_Expires")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    # return token_data
