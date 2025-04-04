"""
This module contains the Client schema
"""

from typing import List, Optional

from pydantic import BaseModel


class Client(BaseModel):
    """
    This is the Client model
    """

    client_id: str
    client_secret: str
    redirect_uris: Optional[List[str]] = None
    grant_types: Optional[List[str]] = None
    response_types: Optional[List[str]] = None
    client_name: Optional[str] = None
    client_uri: Optional[str] = None
    logo_uri: Optional[str] = None
    scope: Optional[List[str]] = None
    contacts: Optional[list[str]] = None
    tos_uri: Optional[str] = None
    policy_uri: Optional[str] = None


class ClientCreate(BaseModel):
    """
    This is the Client model for creation
    """

    client_id: str
    client_secret: str
    redirect_uris: Optional[List[str]] = None
    grant_types: Optional[List[str]] = None
    response_types: Optional[List[str]] = None
    client_name: Optional[str] = None
    client_uri: Optional[str] = None
    logo_uri: Optional[str] = None
    scope: Optional[List[str]] = None
    contacts: Optional[list[str]] = None
    tos_uri: Optional[str] = None
    policy_uri: Optional[str] = None


class ClientUpdate(BaseModel):
    """
    This is the Client model for update
    """

    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    redirect_uris: Optional[List[str]] = None
    grant_types: Optional[List[str]] = None
    response_types: Optional[List[str]] = None
    client_name: Optional[str] = None
    client_uri: Optional[str] = None
    logo_uri: Optional[str] = None
    scope: Optional[List[str]] = None
    contacts: Optional[list[str]] = None
    tos_uri: Optional[str] = None
    policy_uri: Optional[str] = None
