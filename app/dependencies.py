"""
This file contains the dependencies for the FastAPI application.
"""

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlmodel import Session
from app.database import engine
from app.models.token import TokenData
from app.models.user import DBUser
from app.utils import get_user
from app.database import db
from app.utils import oauth2_scheme
from app.conf import SECRET_KEY, ALGORITHM

from sqlalchemy.engine import Engine
from sqlmodel import create_engine

from app.repositories.client import ClientRepository
from app.repositories.user import UserRepository

from app.services.client import ClientService
from app.services.user import UserService


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


def get_session():
    """
    This function gets the session

    :return:
    """
    with Session(engine) as session:
        yield session


def get_engine() -> Engine:
    """
    This function creates and returns a SQLAlchemy engine.
    :return: SQLAlchemy engine
    """
    return create_engine("sqlite:///./test.db")  # Replace with your actual database URL


def get_client_repository(engine_obj: Engine = Depends(get_engine)) -> ClientRepository:
    """
    This function creates and returns a ClientRepository instance.

    :param engine_obj:
    :return:
    """
    return ClientRepository(engine_obj)


def get_user_repository(engine_obj: Engine = Depends(get_engine)) -> UserRepository:
    """
    This function creates and returns a UserRepository instance.

    :param engine_obj:
    :return:
    """
    return UserRepository(engine_obj)


def get_client_service(
    client_repository: ClientRepository = Depends(get_client_repository),
) -> ClientService:
    """
    This function creates and returns a ClientService instance.

    :param client_repository:
    :return:
    """
    return ClientService(client_repository)


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    """
    This function creates and returns a UserService instance.

    :param user_repository:
    :return:
    """
    return UserService(user_repository)

