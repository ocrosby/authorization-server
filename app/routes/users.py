"""
This module contains routes for the User model
"""

from typing import Optional, Sequence

from dependencies import get_user_service
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.status import StatusResponse
from schemas.user import UserUpdate
from services.user import UserService

from app.dependencies import get_current_active_user
from app.models.user import DBUser

router = APIRouter()


@router.get("/me", response_model=DBUser)
async def read_users_me(
    current_user: DBUser = Depends(get_current_active_user),
) -> DBUser:
    """This function reads the current user"""
    return current_user


@router.get("", response_model=Sequence[DBUser])
async def read_users(
    service: UserService = Depends(get_user_service),
    current_user: DBUser = Depends(get_current_active_user),
) -> Sequence[DBUser]:
    """This function reads all users"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to read all users",
        )

    users: Sequence[DBUser] = service.read_all()
    return users


@router.get("/{uid}", response_model=DBUser)
async def read_user(
    uid: int,
    service: UserService = Depends(get_user_service),
    current_user: DBUser = Depends(get_current_active_user),
) -> Optional[DBUser]:
    """This function reads a user by uid"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to read this user",
        )

    user: Optional[DBUser] = service.read(uid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.put("/{uid}", response_model=DBUser)
async def update_user(
    uid: int,
    user: UserUpdate,
    service: UserService = Depends(get_user_service),
    current_user: DBUser = Depends(get_current_active_user),
) -> Optional[DBUser]:
    """This function updates a user by uid"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to update this user",
        )
    updated_user: Optional[DBUser] = service.update(uid, user)
    return updated_user


@router.delete("/{uid}")
async def delete_user(
    uid: int,
    service: UserService = Depends(get_user_service),
    current_user: DBUser = Depends(get_current_active_user),
) -> StatusResponse:
    """This function deletes a user by uid"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete this user",
        )
    service.delete(uid)
    return {"detail": "User deleted"}
