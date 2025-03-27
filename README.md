[build-system]
requires = ["flit_core>=3.2,<4"]
build-backend = "flit_core.buildapi"

[project]
name = "authorization-server"
version = "0.1.0"
description = "A simple OAuth2 authorization server."
authors = [
    { name="Your Name", email="your.email@example.com" }
]
dependencies = [
    "fastapi>=0.70.0",
    "uvicorn>=0.15.0"
]

