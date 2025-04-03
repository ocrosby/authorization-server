"""
This module contains the database configuration
"""

from fastapi import FastAPI
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import SQLModel

from app.dependencies import get_engine

HPW = "$2b$12$MsIdruNFD1BNSED.xG7K1OZTMyg7jNqqGE1T6BxDQwkIv3KhkSGLO"

Base = declarative_base()


def init_db(api_app: FastAPI):
    SQLModel.metadata.create_all(get_engine(), checkfirst=True)
