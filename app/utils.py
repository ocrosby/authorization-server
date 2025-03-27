"""
This module contains utility functions for the application
"""

from datetime import datetime, timedelta, UTC
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from app.models.user import DBUser

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    This function verifies the password

    :param plain_password:
    :param hashed_password:
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    This function gets the password hash

    :param password:
    :return:
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, secret_key: str, algorithm: str, expires_delta: timedelta = None):
    """
    This function creates an access token

    :param data:
    :param secret_key:
    :param algorithm:
    :param expires_delta:
    :return:
    """
    to_encode = data.copy()
    now = datetime.now(UTC)
    expire = now + expires_delta if expires_delta else now + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)

def get_user(_db, username: str) -> Optional[DBUser]:
    """
    This function gets the user

    :param _db:
    :param username:
    :return:
    """
    if username in _db:
        user_data = _db[username]
        return DBUser(**user_data)
    return None

def authenticate_user(_db, username: str, password: str) -> Optional[DBUser]:
    """
    This function authenticates the user

    :param _db:
    :param username:
    :param password:
    :return:
    """
    user = get_user(_db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
