"""
This is the Token model
"""

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
    username: str or None = None
