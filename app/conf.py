"""
This module loads the application settings
"""

import os

from dotenv import load_dotenv

load_dotenv()

# > openssl rand -hex 32
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
ECHO_SQL = os.getenv("ECHO_SQL", "false").lower() == "true"
DATABASE_URL = os.getenv("DATABASE_URL")
BASE_URL = os.getenv("BASE_URL")
