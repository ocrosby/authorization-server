"""
This module contains routes for the User model
"""

from fastapi import APIRouter, Depends
from app.models.user import DBUser
from app.dependencies import get_current_active_user, verify_current_user

router = APIRouter()


@router.get("/users/me/", response_model=DBUser)
async def read_users_me(current_user: DBUser = Depends(get_current_active_user)):
    """This function reads the current user"""
    return current_user


@router.get("/users/me/items")
async def read_own_items(current_user: DBUser = Depends(get_current_active_user)):
    """This function reads the current user's items"""
    return [{"item_id": "Foo", "owner": current_user}]
