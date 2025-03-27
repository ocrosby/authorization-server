"""
This module contains the User model
"""

from pydantic import BaseModel

class User(BaseModel):
    """
    This is the User model
    """
    username: str
    email: str or None = None
    full_name: str or None = None
    disabled: bool or None = None

class DBUser(User):
    """
    This is the DBUser model
    """
    hashed_password: str
    