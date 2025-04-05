"""
This module contains the Status schema
"""

from typing import Optional

from pydantic import BaseModel


class StatusResponse(BaseModel):
    """
    This is the Status model
    """

    status: Optional[str] = None
