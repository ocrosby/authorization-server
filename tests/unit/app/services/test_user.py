"""
This module contains tests for the user service.
"""

import pytest

from app.models.user import DBUser
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.services.user import UserService


@pytest.fixture
def mock_repository(mocker):
    """
    Create a mock user repository

    :param mocker:
    :return:
    """
    return mocker.Mock()


@pytest.fixture
def user_service(mock_repository: UserRepository) -> UserService:
    """
    This fixture creates a user service

    :param mock_repository:
    :return:
    """
    return UserService(mock_repository)


@pytest.fixture
def mock_db_user(mocker):
    """
    This fixture creates a mock user

    :param mocker:
    :return:
    """
    mock_user = mocker.Mock()

    mock_user.username = "newuser"
    mock_user.email = "newuser@example.com"
    mock_user.hashed_password = "hash"

    return mock_user


@pytest.fixture
def test_db_user():
    """
    This fixture creates a test user

    :return:
    """
    return DBUser(
        username="newuser",
        email="newuser@example.com",
        hashed_password="hash",
    )


@pytest.fixture
def user_create():
    """
    This fixture creates a mock user create

    :return:
    """
    return UserCreate(
        username="newuser",
        email="newuser@example.com",
        password="newpassword",
    )


@pytest.fixture
def user_update():
    """
    This fixture creates a mock user update

    :return:
    """
    return UserUpdate(
        username="updateduser",
        email="updateduser@example.com",
        password="updatedpassword",
    )


def test_create(mock_repository, user_create, user_service, mock_db_user) -> None:
    """
    This function tests the create method of the user service.

    :param mock_repository:
    :param user_create:
    :param user_service:
    :param mock_db_user:
    :return:
    """
    # Arrange
    mock_repository.create.return_value = mock_db_user

    # Act
    result = user_service.create(user_create)

    # Assert
    assert result == mock_db_user
    mock_repository.create.assert_called_once_with(user_create)


def test_read(mock_repository, user_service, test_db_user):
    """
    This function tests the read method of the user service.

    :param mock_repository:
    :param user_service:
    :param test_db_user:
    :return:
    """
    # Arrange
    uid = 1
    mock_repository.read.return_value = test_db_user

    # Act
    result = user_service.read(uid)

    # Assert
    assert result.username == test_db_user.username
    assert result.email == test_db_user.email
    assert result.hashed_password == test_db_user.hashed_password

    mock_repository.read.assert_called_once_with(uid)


def test_read_by_username(mock_repository, user_service, test_db_user):
    """
    This function tests the read_by_username method of the user service.

    :param mock_repository:
    :param user_service:
    :param test_db_user:
    :return:
    """
    # Arrange
    username = "newuser"
    mock_repository.read_by_username.return_value = test_db_user

    # Act
    result = user_service.read_by_username(username)

    # Assert
    assert result.username == test_db_user.username
    assert result.email == test_db_user.email
    assert result.hashed_password == test_db_user.hashed_password

    mock_repository.read_by_username.assert_called_once_with(username)


def test_read_by_email(mock_repository, user_service, test_db_user):
    """
    This function tests the read_by_email method of the user service.

    :param mock_repository:
    :param user_service:
    :param test_db_user:
    :return:
    """
    # Arrange
    email = "newuser@example.com"
    mock_repository.read_by_email.return_value = test_db_user

    # Act
    result = user_service.read_by_email(email)

    # Assert
    assert result.username == test_db_user.username
    assert result.email == test_db_user.email
    assert result.hashed_password == test_db_user.hashed_password

    mock_repository.read_by_email.assert_called_once_with(email)


def test_read_all(mock_repository, user_service, test_db_user):
    """
    This function tests the read_all method of the user service.

    :param mock_repository:
    :param user_service:
    :param test_db_user:
    :return:
    """
    # Arrange
    mock_repository.read_all.return_value = [test_db_user]

    # Act
    result = user_service.read_all()

    # Assert
    assert len(result) == 1
    assert result[0].username == test_db_user.username
    assert result[0].email == test_db_user.email
    assert result[0].hashed_password == test_db_user.hashed_password

    mock_repository.read_all.assert_called_once()


def test_update(mock_repository, user_service, user_update, test_db_user):
    """
    This function tests the update method of the user service.

    :param mock_repository:
    :param user_service:
    :param user_update:
    :param test_db_user:
    :return:
    """
    # Arrange
    uid = 1
    mock_repository.update.return_value = test_db_user

    # Act
    result = user_service.update(uid, user_update)

    # Assert
    assert result is not None
    assert result == test_db_user
    mock_repository.update.assert_called_once_with(uid, user_update)


@pytest.mark.parametrize(
    "uid, expected_result",
    [
        (1, True),  # Existing user ID
        (999, False),  # Non-existing user ID
    ],
    ids=["Existing user ID", "Non-existing user ID"],
)
def test_delete(uid, expected_result, mock_repository, user_service):
    """
    This function tests the delete method of the user service.

    :param uid:
    :param expected_result:
    :param mock_repository:
    :param user_service:
    :return:
    """
    # Arrange
    mock_repository.delete.return_value = expected_result

    # Act
    result = user_service.delete(uid)

    # Assert
    assert result is expected_result
    mock_repository.delete.assert_called_once_with(uid)
