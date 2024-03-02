from fastapi import Depends, HTTPException, status, Response
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from . import jwt_token
from settings import database
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):

    return jwt_token.verify_token
