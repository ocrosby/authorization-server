"""
This module contains the User schema
"""

from typing import Optional

from pydantic import BaseModel


class UserDisplay(BaseModel):
    """
    This is the User model for display
    """

    id: Optional[int] = None
    username: str
    email: str
    disabled: Optional[bool] = False

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    """
    This is the User model for creation
    """

    username: str
    email: str
    password: str
    disabled: Optional[bool] = False


class UserUpdate(BaseModel):
    """
    This is the User model for update
    """

    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    disabled: Optional[bool] = False


class UserLogin(BaseModel):
    """
    This is the UserLogin model
    """

    username: str
    password: str
