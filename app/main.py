"""
This is the main file for the FastAPI application
"""
import os
from contextlib import asynccontextmanager

import toml
import uvicorn

from fastapi import FastAPI

from app.database import init_db
from app.routes import auth, user


def get_project_metadata():
    """
    Reads the pyproject.toml file to extract project metadata.

    :return: description, version, author_name, author_email
        - description: Project description
        - version: Project version
        - author_name: Author's name
        - author_email: Author's email
    """
    with open("pyproject.toml", "r", encoding="utf-8") as f:
        pyproject_data = toml.load(f)

    project_data = pyproject_data.get("project", {})
    description = project_data.get("description", "No description available")
    version = project_data.get("version", "0.0.0")
    authors = project_data.get("authors", [{}])
    author_name = authors[0].get("name", "Unknown author")
    author_email = authors[0].get("email", "Unknown email")

    return description, version, author_name, author_email


description, version, author_name, author_email = get_project_metadata()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for the FastAPI application.
    This function is called when the application starts up and shuts down.
    It can be used to perform setup and teardown tasks.
    For example, you can use it to initialize a database connection or load configuration files.

    :param app: FastAPI
    :return:
    """
    init_db()

    print("Swagger UI: http://127.0.0.1:8000/docs")
    print("ReDoc: http://127.0.0.1:8000/redoc")

    yield
    # Add any cleanup code here if needed


app = FastAPI(
    title="Authorization Server",
    description=description,
    version=version,
    contact={
        "name": author_name,
        "email": author_email,
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan
)

# Include routers
app.include_router(auth.router)
app.include_router(user.router)


def main():
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
