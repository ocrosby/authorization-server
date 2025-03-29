"""
This module contains the User schema
"""

from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    """
    This is the User model
    """

    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = False
    hashed_password: Optional[str] = None


class UserCreate(BaseModel):
    """
    This is the User model for creation
    """

    username: str
    email: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = False
    password: str


class UserUpdate(BaseModel):
    """
    This is the User model for update
    """

    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = False
    hashed_password: Optional[str] = None


class UserLogin(BaseModel):
    """
    This is the UserLogin model
    """

    username: str
    password: str
