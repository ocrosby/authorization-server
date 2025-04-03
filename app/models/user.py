"""
This module contains the User model
"""

from typing import Optional

from sqlmodel import Field, SQLModel


class DBUser(SQLModel, table=True):
    """
    The database model for the User
    """

    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    disabled: Optional[bool] = False
    hashed_password: Optional[str] = None
