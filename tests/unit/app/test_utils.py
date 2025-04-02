"""
This module contains unit tests for the utility functions in app.utils.
"""

from datetime import UTC, datetime, timedelta

import pytest

from app.utils import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_user,
    verify_password,
)


@pytest.fixture
def mock_pwd_context(mocker):
    return mocker.patch("app.utils.pwd_context")


@pytest.fixture
def mock_jwt(mocker):
    return mocker.patch("app.utils.jwt")


@pytest.fixture
def mock_datetime(mocker):
    return mocker.patch("app.utils.datetime")


def test_verify_password(mock_pwd_context):
    """
    Test the verify_password function.
    """
    # Arrange
    mock_pwd_context.verify.return_value = True

    # Act
    result = verify_password("plain_password", "hashed_password")

    # Assert
    assert result is True
    mock_pwd_context.verify.assert_called_once_with("plain_password", "hashed_password")


def test_get_password_hash(mock_pwd_context):
    """
    Test the get_password_hash function.
    """
    # Arrange
    mock_pwd_context.hash.return_value = "hashed_password"

    # Act
    result = get_password_hash("plain_password")

    # Assert
    assert result == "hashed_password"
    mock_pwd_context.hash.assert_called_once_with("plain_password")


def test_create_access_token(mock_jwt, mock_datetime):
    """
    Test the create_access_token function with expiration.
    """
    # Arrange
    mock_datetime.now.return_value = datetime(2023, 1, 1, tzinfo=UTC)
    mock_jwt.encode.return_value = "token"
    data = {"sub": "user"}
    secret_key = "secret"
    algorithm = "HS256"
    expires_delta = timedelta(minutes=30)

    # Act
    token = create_access_token(data, secret_key, algorithm, expires_delta)

    # Assert
    assert token == "token"
    mock_jwt.encode.assert_called_once()
    mock_datetime.now.assert_called_once()


def test_create_access_token_no_expiration(mock_jwt, mock_datetime):
    """
    Test the create_access_token function without expiration.
    """
    # Arrange
    mock_datetime.now.return_value = datetime(2023, 1, 1, tzinfo=UTC)
    mock_jwt.encode.return_value = "token"
    data = {"sub": "user"}
    secret_key = "secret"
    algorithm = "HS256"

    # Act
    token = create_access_token(data, secret_key, algorithm)

    # Assert
    assert token == "token"
    mock_jwt.encode.assert_called_once()
    mock_datetime.now.assert_called_once()


# def test_get_user():
#     """
#     Test the get_user function.
#     """
#     # Arrange
#     _db = {"testuser": {"id": 1, "username": "testuser", "hashed_password": "hashed"}}
#
#     # Act
#     user = get_user(_db, "testuser")
#
#     # Assert
#     assert user.id == 1
#     assert user.username == "testuser"


# def test_get_user_not_found():
#     """
#     Test the get_user function when the user is not found.
#     """
#     # Arrange
#     _db = {}
#
#     # Act
#     user = get_user(_db, "testuser")
#
#     # Assert
#     assert user is None


# def test_authenticate_user(mocker):
#     """
#     Test the authenticate_user function.
#     """
#     # Arrange
#     _db = {"testuser": {"id": 1, "username": "testuser", "hashed_password": "hashed"}}
#     mocker.patch("app.utils.verify_password", return_value=True)
#
#     # Act
#     user = authenticate_user(_db, "testuser", "password")
#
#     # Assert
#     assert user.username == "testuser"


# def test_authenticate_user_invalid_password(mocker):
#     """
#     Test the authenticate_user function with an invalid password.
#     """
#     # Arrange
#     _db = {"testuser": {"id": 1, "username": "testuser", "hashed_password": "hashed"}}
#     mocker.patch("app.utils.verify_password", return_value=False)
#
#     # Act
#     user = authenticate_user(_db, "testuser", "password")
#
#     # Assert
#     assert user is None


# def test_authenticate_user_not_found():
#     """
#     Test the authenticate_user function when the user is not found.
#     """
#     # Arrange
#     _db = {}
#
#     # Act
#     user = authenticate_user(_db, "testuser", "password")
#
#     # Assert
#     assert user is None
