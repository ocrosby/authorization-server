"""
This module contains routes for the Client model
"""

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.models.user import DBUser
from app.models.client import DBClient
from app.schemas.client import ClientCreate, ClientUpdate
from app.services.client import ClientService
from app.dependencies import get_current_active_user, verify_current_user, get_session, get_client_service


router = APIRouter()


@router.post("/", response_model=DBClient)
async def create_client(
    client: ClientCreate,
    db: Session = Depends(get_session),
    current_user: DBUser = Depends(get_current_active_user),
):
    """This function creates a new client"""
    verify_current_user(current_user)

    db_client = DBClient(
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
        policy_uri=client.policy_uri,
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)

    return client


@router.get("/{client_id}", response_model=DBClient)
async def read_client(
    client_id: int, service: ClientService = Depends(get_client_service)
):
    """This function reads a client"""
    return service.read(client_id)


@router.put("/{client_id}", response_model=DBClient)
async def update_client(
    client_id: int,
    client: ClientUpdate,
    service: ClientService = Depends(get_client_service),
    current_user: DBUser = Depends(get_current_active_user),
):
    """This function updates a client"""
    verify_current_user(current_user)

    return service.update(client_id, client)


@router.delete("/{client_id}")
async def delete_client(
    client_id: int,
    service: ClientService = Depends(get_client_service),
    current_user: DBUser = Depends(get_current_active_user),
):
    """This function deletes a client"""
    verify_current_user(current_user)

    return service.delete(client_id)
