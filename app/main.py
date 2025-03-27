"""
This is the main file for the FastAPI application
"""

import os

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from app.utils import get_password_hash
from app.routes import auth, user

load_dotenv()

# > openssl rand -hex 32
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# defines where we go to retrieve our access token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

# Include routers
app.include_router(auth.router)
app.include_router(user.router)

if __name__ == "__main__":
    pwd = get_password_hash("tim1234")
    print(pwd)
