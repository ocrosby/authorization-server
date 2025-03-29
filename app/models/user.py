"""
This module contains the User model
"""

from typing import Optional
from sqlmodel import SQLModel, Field


class DBUser(SQLModel, table=True):
    """
    The database model for the User
    """

    __tablename__ = "users"

    id: int = Field(primary_key=True, sa_column_kwargs={"autoincrement": True})
    username: str = Field(index=True, unique=True, nullable=False)
    email: Optional[str] = Field(index=True, unique=True, nullable=False)
    full_name: Optional[str] = Field(default=None)
    disabled: Optional[bool] = Field(default=False, nullable=False)
    hashed_password: str = Field(nullable=False)
