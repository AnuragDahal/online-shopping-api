from fastapi import Request, Response, HTTPException, status
from fastapi import HTTPException, status, Request, Response
from jose import JWTError, jwt
from datetime import datetime, timedelta
from config import schemas
import os
from dotenv import load_dotenv

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


# async def verify_token(req: Request, res: Response):
#     try:
#         token = req.cookies.get("token")

#         payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
#         res=await
#         email: str = payload.get("sub")
#         if email is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Could not validate credentials: 'sub' claim missing",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#         token_data = schemas.TokenData(email=email)
#         return token_data
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )


async def verify_token(req: Request, res: Response):
    try:
        token = req.cookies.get("token")

        if token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials: Token missing",
                headers={"WWW-Authenticate": "Bearer"},
            )

        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials: 'sub' claim missing",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token_data = schemas.TokenData(email=email)
        # req.state.token_data = token_data  # Store the token_data in the request state
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return res
