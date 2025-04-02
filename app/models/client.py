"""
This module contains the Client model
"""

from typing import List, Optional

from sqlalchemy import Column, Text
from sqlmodel import Field, SQLModel
import json

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
    redirect_uris: Optional[List[str]] = Field(sa_column=Column(Text))
    grant_types: Optional[List[str]] = Field(sa_column=Column(Text))
    response_types: Optional[List[str]] = Field(sa_column=Column(Text))
    client_name: Optional[str] = None
    client_uri: Optional[str] = None
    logo_uri: Optional[str] = None
    scope: Optional[List[str]] = Field(sa_column=Column(Text))
    contacts: Optional[List[str]] = Field(sa_column=Column(Text), default=None)
    tos_uri: Optional[str] = None
    policy_uri: Optional[str] = None

    @property
    def redirect_uris_list(self) -> List[str]:
        return json.loads(self.redirect_uris) if self.redirect_uris else []

    @redirect_uris_list.setter
    def redirect_uris_list(self, value: List[str]):
        self.redirect_uris = json.dumps(value)

    @property
    def grant_types_list(self) -> List[str]:
        return json.loads(self.grant_types) if self.grant_types else []

    @grant_types_list.setter
    def grant_types_list(self, value: List[str]):
        self.grant_types = json.dumps(value)

    @property
    def response_types_list(self) -> List[str]:
        return json.loads(self.response_types) if self.response_types else []

    @response_types_list.setter
    def response_types_list(self, value: List[str]):
        self.response_types = json.dumps(value)

    @property
    def scope_list(self) -> List[str]:
        return json.loads(self.scope) if self.scope else []

    @scope_list.setter
    def scope_list(self, value: List[str]):
        self.scope = json.dumps(value)

    @property
    def contacts_list(self) -> List[str]:
        return json.loads(self.contacts) if self.contacts else []

    @contacts_list.setter
    def contacts_list(self, value: List[str]):
        self.contacts = json.dumps(value)