"""
This module contains routes for the User model
"""

from typing import Sequence

from dependencies import get_user_service
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user import UserUpdate
from services.user import UserService
from utils import oauth2_scheme

from app.dependencies import get_current_active_user
from app.models.user import DBUser

router = APIRouter()


@router.get("/me", response_model=DBUser)
async def read_users_me(current_user: DBUser = Depends(get_current_active_user)):
    """This function reads the current user"""
    return current_user


@router.get("", response_model=Sequence[DBUser])
async def read_users(
    service: UserService = Depends(get_user_service),
    current_user: DBUser = Depends(get_current_active_user),
):
    """This function reads all users"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to read all users",
        )

    return service.read_all()


@router.get("/{uid}", response_model=DBUser)
async def read_user(
    uid: str,
    service: UserService = Depends(get_user_service),
    current_user: DBUser = Depends(get_current_active_user),
):
    """This function reads a user by uid"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to read this user",
        )

    user = service.read(uid)
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
):
    """This function updates a user by uid"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to update this user",
        )
    return service.update(uid, user)


@router.delete("/{uid}")
async def delete_user(
    uid: int,
    service: UserService = Depends(get_user_service),
    current_user: DBUser = Depends(get_current_active_user),
):
    """This function deletes a user by uid"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete this user",
        )
    service.delete(uid)
    return {"detail": "User deleted"}
