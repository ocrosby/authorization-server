"""
This module contains the Client model
"""

from typing import Optional

from sqlalchemy import Column, Text
from sqlmodel import Field, SQLModel


class DBClient(SQLModel, table=True):
    """
    OAuth2 Client model

    The fields are described below

    id: int - the primary key
    client_id: str - the client ID
    client_secret: str - the client secret
    redirect_uris: List[str] - the redirect URIs
    grant_types: List[str] - the grant types
    response_types: List[str] - the response types
    client_name: str - the client name
    client_uri: Optional[str] - the client URI
    logo_uri: Optional[str] - the logo URI
    scope: list[str] - the scope
    contacts: Optional[List[str]] - the contacts
    tos_uri: Optional[str] - the terms of service URI
    policy_uri: Optional[str] - the policy URI
    """

    __tablename__ = "clients"

    id: int = Field(default=None, primary_key=True)
    client_id: str
    client_secret: str
    redirect_uris: Optional[str] = Field(sa_column=Column(Text))
    grant_types: Optional[str] = Field(sa_column=Column(Text))
    response_types: Optional[str] = Field(sa_column=Column(Text))
    client_name: Optional[str] = None
    client_uri: Optional[str] = None
    logo_uri: Optional[str] = None
    scope: Optional[str] = Field(sa_column=Column(Text))
    contacts: Optional[str] = Field(sa_column=Column(Text), default=None)
    tos_uri: Optional[str] = None
    policy_uri: Optional[str] = None
