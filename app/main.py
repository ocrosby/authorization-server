"""
This is the main file for the FastAPI application
"""

import os
from datetime import datetime, timedelta, UTC
from typing import Optional

from dotenv import load_dotenv

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from jose import JWTError, jwt
from passlib.context import CryptContext

load_dotenv()

# > openssl rand -hex 32
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

HPW = "$2b$12$MsIdruNFD1BNSED.xG7K1OZTMyg7jNqqGE1T6BxDQwkIv3KhkSGLO"
db = {
    "tim": {
        "username": "tim",
        "full_name": "Timothy McTimmerson",
        "email": "tim@gmail.com",
        "hashed_password": HPW,
        "disabled": False # You've signed in but your access token is expired
    }
}

class Token(BaseModel):
    """
    This is the Token model
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    This is the TokenData model
    """
    username: str or None = None

class User(BaseModel):
    """
    This is the User model
    """
    username: str
    email: str or None = None
    full_name: str or None = None
    disabled: bool or None = None

class UserInDB(User):
    """
    Inherits from User class
    """
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# defines where we go to retrieve our access token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    This function verifies the password

    :param plain_password:
    :param hashed_password:
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    This function gets the password hash

    :param password:
    :return:
    """
    return pwd_context.hash(password)

def get_user(_db, username: str) -> Optional[UserInDB]:
    """
    This function gets the user

    :param _db:
    :param username:
    :return:
    """
    if username in _db:
        user_data = _db[username]
        return UserInDB(**user_data)

    return None

def authenticate_user(_db, username: str, password: str) -> Optional[UserInDB]:
    """
    This function authenticates the user

    :param _db:
    :param username:
    :param password:
    :return:
    """
    user = get_user(_db, username)
    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    This function creates the access token

    :param data:
    :param expires_delta:
    :return:
    """
    to_encode = data.copy()

    now = datetime.now(UTC)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    This function gets the current user

    :param token:
    :return:
    """
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credential_exception

        token_data = TokenData()
        token_data.username = username
    except JWTError as err:
        raise credential_exception from err

    user = get_user(db, username=token_data.username)
    if user is None:
        raise credential_exception

    return user

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    """
    This function gets the current active user

    :param current_user:
    :return:
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    This function logs in for access token

    :param form_data:
    :return:
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    This function reads the user

    :param current_user:
    :return:
    """
    return current_user

@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    """
    This function reads the own items

    :param current_user:
    :return:
    """
    return [{"item_id": "Foo", "owner": current_user}]

if __name__ == "__main__":
    pwd = get_password_hash("tim1234")
    print(pwd)
