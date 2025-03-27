"""
This module contains routes for the Client model
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.models.client import Client
from app.dependencies import get_session


router = APIRouter()


class ClientCreate(BaseModel):
    """
    This is the ClientCreate model
    """
    client_id: str
    client_secret: str
    redirect_uris: list[str]
    grant_types: list[str]
    response_types: list[str]
    client_name: str
    client_uri: str or None = None
    logo_uri: str or None = None
    scope: list[str]
    contacts: list[str] or None = None
    tos_uri: str or None = None
    policy_uri: str or None = None


@router.post("/", response_model=Client)
async def create_client(client: ClientCreate, db: Session = Depends(get_session)):
    """This function creates a new client"""
    db_client = Client(
        client_id=client.client_id,
        client_secret=client.client_secret,
        redirect_uris=client.redirect_uris,
        grant_types=client.grant_types,
        response_types=client.response_types,
        client_name=client.client_name,
        client_uri=client.client_uri,
        logo_uri=client.logo_uri,
        scope=client.scope,
        contacts=client.contacts,
        tos_uri=client.tos_uri,
        policy_uri=client.policy_uri
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)

    return client

@router.get("/{client_id}", response_model=Client)
async def read_client(client_id: str):
    """This function reads a client"""
    return {"client_id": client_id}

@router.put("/{client_id}", response_model=Client)
async def update_client(client_id: str, client: Client):
    """This function updates a client"""
    return client

@router.delete("/{client_id}")
async def delete_client(client_id: str):
    """This function deletes a client"""
    return {"client_id": client_id}
