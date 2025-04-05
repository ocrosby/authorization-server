"""
This module contains routes for the Client model
"""

from typing import Optional, Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import (
    get_client_service,
    get_current_active_user,
    get_session,
)
from app.models.client import DBClient
from app.models.user import DBUser
from app.schemas.client import ClientCreate, ClientUpdate
from app.services.client import ClientService

router = APIRouter()


@router.get("", response_model=list[DBClient])
async def read_clients(
    current_user: DBUser = Depends(get_current_active_user),  # noqa: F841
    service: ClientService = Depends(get_client_service),
) -> Sequence[DBClient]:
    """This function reads all clients"""
    return service.read_all()


@router.post("", response_model=DBClient)
async def create_client(
    client_create: ClientCreate,
    db: Session = Depends(get_session),
    current_user: DBUser = Depends(get_current_active_user),  # noqa: F841
) -> DBClient:
    """This function creates a new client"""
    db_client = DBClient(
        client_id=client_create.client_id,
        client_secret=client_create.client_secret,
        redirect_uris=client_create.redirect_uris,
        grant_types=client_create.grant_types,
        response_types=client_create.response_types,
        client_name=client_create.client_name,
        client_uri=client_create.client_uri,
        logo_uri=client_create.logo_uri,
        scope=client_create.scope,
        contacts=client_create.contacts,
        tos_uri=client_create.tos_uri,
        policy_uri=client_create.policy_uri,
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)

    return db_client


@router.get("/{client_id}", response_model=DBClient)
async def read_client(
    client_id: int, service: ClientService = Depends(get_client_service)
) -> Optional[DBClient]:
    """This function reads a client"""
    return service.read(client_id)


@router.put("/{client_id}", response_model=DBClient)
async def update_client(
    client_id: int,
    client: ClientUpdate,
    service: ClientService = Depends(get_client_service),
    current_user: DBUser = Depends(get_current_active_user),  # noqa: F841
) -> Optional[DBClient]:
    """This function updates a client"""
    return service.update(client_id, client)


@router.delete("/{client_id}")
async def delete_client(
    client_id: int,
    service: ClientService = Depends(get_client_service),
    current_user: DBUser = Depends(get_current_active_user),  # noqa: F841
) -> None:
    """This function deletes a client"""
    service.delete(client_id)
    return None
