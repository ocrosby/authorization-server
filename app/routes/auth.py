"""
This module contains the routes for authentication
"""

from datetime import timedelta

from dependencies import get_user_service
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models.user import DBUser
from schemas.user import UserCreate
from services.user import UserService

from app.conf import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from app.models.token import Token
from app.utils import authenticate_user, create_access_token, register_user

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service),
):
    """This function logs in for access token"""
    user = authenticate_user(service, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": user.username},
        secret_key=SECRET_KEY,
        algorithm=ALGORITHM,
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=DBUser)
async def create_user(
    user: UserCreate,
    service: UserService = Depends(get_user_service),
):
    """This function registers a new user"""
    new_user = register_user(service, user.username, user.password, user.email)

    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered",
        )

    return new_user
