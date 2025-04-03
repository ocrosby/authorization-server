"""
This module contains the Status schema
"""

from typing import Optional

from pydantic import BaseModel


class StatusResponse(BaseModel):
    status: Optional[str] = None
