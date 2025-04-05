# OAuth2 Authorization Server

[![Continuous Integration](https://github.com/ocrosby/authorization-server/actions/workflows/ci.yaml/badge.svg)](https://github.com/ocrosby/authorization-server/actions/workflows/ci.yaml)
[![Release](https://github.com/ocrosby/authorization-server/actions/workflows/release.yaml/badge.svg)](https://github.com/ocrosby/authorization-server/actions/workflows/release.yaml)

A simple OAuth2 authorization server.

## Project Description

This project is an OAuth2 authorization server built with FastAPI. It includes features such as password hashing and token generation.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/ocrosby/authorization-server.git
    cd authorization-server
    ```

2. Create and activate a virtual environment:
    ```sh
    python3.13 -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install --upgrade pip
    pip install invoke flit
    pip install -e ".[dev]"
    ```

## Configuration

1. Create a `.env` file in the root directory of the project and add the following environment variables:
    ```dotenv
    SECRET_KEY=your_secret_key_here
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

2. You can use the `sample.env` file as a template for your environment variables.

## Usage

1. Run the FastAPI server:
    ```sh
    uvicorn app.main:app --reload
    ```

2. Use the `hashpwd` CLI command to hash a password:
    ```sh
    hashpwd your_password
    ```

## Testing

Run the tests using pytest:
```sh
pytest
```

## References

- [OAuth 2.0](https://oauth.net/2/)