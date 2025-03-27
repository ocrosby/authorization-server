"""
This is the main file for the FastAPI application
"""

from dotenv import load_dotenv

from fastapi import FastAPI

from app.utils import get_password_hash
from app.routes import auth, user

load_dotenv()

app = FastAPI()

# Include routers
app.include_router(auth.router)
app.include_router(user.router)

if __name__ == "__main__":
    pwd = get_password_hash("tim1234")
    print(pwd)
