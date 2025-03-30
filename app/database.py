"""
This module contains the database configuration
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import create_engine

from app.conf import DATABASE_URL

HPW = "$2b$12$MsIdruNFD1BNSED.xG7K1OZTMyg7jNqqGE1T6BxDQwkIv3KhkSGLO"
db = {
    "tim": {
        "username": "tim",
        "full_name": "Timothy McTimmerson",
        "email": "tim@gmail.com",
        "hashed_password": HPW,
        "disabled": False,
    }
}

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
