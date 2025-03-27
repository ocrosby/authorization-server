"""
This file contains the dependencies for the FastAPI application.
"""

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from app.models.token import TokenData
from app.models.user import DBUser
from app.utils import get_user
from app.database import db
from app.main import oauth2_scheme
from app.conf import SECRET_KEY, ALGORITHM

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    This function gets the current user

    :param token:
    :return:
    """
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credential_exception

        token_data = TokenData()
        token_data.username = username
    except JWTError as err:
        raise credential_exception from err

    user = get_user(db, username=token_data.username)
    if user is None:
        raise credential_exception

    return user

async def get_current_active_user(current_user: DBUser = Depends(get_current_user)):
    """
    This function gets the current active user

    :param current_user:
    :return:
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user
