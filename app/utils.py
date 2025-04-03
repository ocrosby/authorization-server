"""
This module contains utility functions for the application
"""

import os
from datetime import UTC, datetime, timedelta
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from app.models.user import DBUser
from app.services.user import UserService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def find_root_directory() -> Optional[str]:
    """
    This function finds the root directory of the project

    :return:
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    while current_dir != "/":
        if os.path.exists(os.path.join(current_dir, "pyproject.toml")):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    return None


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


def create_access_token(
    data: dict, secret_key: str, algorithm: str, expires_delta: timedelta = None
) -> str:
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


def get_user(service: UserService, username: str) -> Optional[DBUser]:
    """
    This function gets the user

    :param service:
    :param username:
    :return:
    """
    return service.read_by_username(username=username)


def authenticate_user(
    service: UserService, username: str, password: str
) -> Optional[DBUser]:
    """
    This function authenticates the user

    :param service:
    :param username:
    :param password:
    :return:
    """
    user = get_user(service, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def register_user(
    service: UserService, username: str, password: str, email: str
) -> Optional[DBUser]:
    """
    This function registers the user

    :param service:
    :param username:
    :param password:
    :param email:
    :return:
    """
    if service.read_by_username(username=username):
        return None
    if service.read_by_email(email=email):
        return None
    hashed_password = get_password_hash(password)
    user = DBUser(username=username, hashed_password=hashed_password, email=email)
    service.create(user)
    return user
