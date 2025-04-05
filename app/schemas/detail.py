"""
This module contains the Detail schema
"""

from typing import Optional

from pydantic import BaseModel


class DetailResponse(BaseModel):
    """
    This is the Detail model
    """

    detail: Optional[str] = None
