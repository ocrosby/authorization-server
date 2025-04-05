"""
This is the main file for the FastAPI application
"""

import os
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Tuple

import toml
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils import find_root_directory

from app.conf import DATABASE_URL
from app.database import init_db
from app.routes import auth, clients, probes, users


def get_project_metadata() -> Tuple[str, str, str, str]:
    """
    Reads the pyproject.toml file to extract project metadata.

    :return: description, version, author_name, author_email
        - description: Project description
        - version: Project version
        - author_name: Author's name
        - author_email: Author's email
    """
    root_directory = find_root_directory()
    project_file = os.path.join(root_directory, "pyproject.toml")
    with open(project_file, "r", encoding="utf-8") as f:
        pyproject_data = toml.load(f)

    project_data = pyproject_data.get("project", {})
    project_description = project_data.get("description", "No description available")
    project_version = project_data.get("version", "0.0.0")
    project_authors = project_data.get("authors", [{}])
    project_author_name = project_authors[0].get("name", "Unknown author")
    project_author_email = project_authors[0].get("email", "Unknown email")

    return (
        project_description,
        project_version,
        project_author_name,
        project_author_email,
    )


description, version, author_name, author_email = get_project_metadata()


@asynccontextmanager
async def lifespan(api_app: FastAPI) -> AsyncGenerator[None, Any]:  # noqa: D103
    """
    Lifespan event handler for the FastAPI application.
    This function is called when the application starts up and shuts down.
    It can be used to perform setup and teardown tasks.
    For example, you can use it to initialize a database connection or load configuration files.

    :param api_app: FastAPI
    """
    print("Starting up the application...")
    print(f"Database URL: {DATABASE_URL}")
    print("Swagger UI: http://127.0.0.1:8000/docs")
    print("ReDoc: http://127.0.0.1:8000/redoc")

    yield
    # Add any cleanup code here if needed


tags_metadata = [
    {
        "name": "auth",
        "description": "Authentication routes",
    },
    {
        "name": "users",
        "description": "User management routes",
    },
    {
        "name": "probes",
        "description": "Health check routes",
    },
    {
        "name": "clients",
        "description": "Client management routes",
    },
]

# Define the allowed origins
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://yourdomain.com",
]

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
    lifespan=lifespan,
    openapi_tags=tags_metadata,
)

# Add CORS middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the database
init_db(app)

# Include routers
app.include_router(auth.router, tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(probes.router, prefix="/health", tags=["probes"])
app.include_router(clients.router, prefix="/clients", tags=["clients"])


def main() -> None:
    """
    Main function to run the FastAPI application.
    :return:
    """
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
