"""
This is the Token model
"""

from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """
    This is the Token model
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    This is the TokenData model
    """

    username: Optional[str] = None
