"""
This module contains the unit tests for the UserRepository class.
"""

# tests/unit/app/repositories/test_user.py

import pytest
from schemas.user import UserCreate, UserUpdate
from utils import verify_password

from app.models.user import DBUser
from app.repositories.user import UserRepository
from app.security import get_password_hash

# from app.schemas.user import User


@pytest.fixture
def mock_session(mocker):
    """
    Fixture to mock the SQLModel Session.

    :param mocker: The pytest-mock mocker fixture.
    :return: Mocked Session.
    """
    return mocker.patch("app.repositories.user.Session", autospec=True)


@pytest.fixture
def user_repository(mock_engine):
    """
    Fixture to create a UserRepository instance with a mocked engine.

    :param mock_engine: The mocked engine fixture.
    :return: UserRepository instance.
    """
    return UserRepository(mock_engine)


def test_read(user_repository, mock_session):
    """
    Test the read method of UserRepository.

    :param user_repository: The UserRepository instance.
    :param mock_session: The mocked Session fixture.
    """
    # Arrange
    mock_session_instance = mock_session.return_value.__enter__.return_value
    mock_session_instance.get.return_value = DBUser(id=1, username="testuser")

    # Act
    user = user_repository.read(1)

    # Assert
    assert user.id == 1
    assert user.username == "testuser"


def test_read_by_username(user_repository, mock_session):
    """
    Test the read_by_username method of UserRepository.

    :param user_repository: The UserRepository instance.
    :param mock_session: The mocked Session fixture.
    """
    # Arrange
    mock_session.return_value.__enter__.return_value.exec.return_value.first.return_value = DBUser(
        id=1, username="testuser"
    )

    # Act
    user = user_repository.read_by_username("testuser")

    # Assert
    assert user.id == 1
    assert user.username == "testuser"


def test_read_by_email(user_repository, mock_session):
    """
    Test the read_by_email method of UserRepository.

    :param user_repository: The UserRepository instance.
    :param mock_session: The mocked Session fixture.
    """
    # Arrange
    mock_session.return_value.__enter__.return_value.exec.return_value.first.return_value = DBUser(
        id=1, email="test@example.com"
    )

    # Act
    user = user_repository.read_by_email("test@example.com")

    # Assert
    assert user.id == 1
    assert user.email == "test@example.com"


def test_read_all(user_repository, mock_session):
    """
    Test the read_all method of UserRepository.

    :param user_repository: The UserRepository instance.
    :param mock_session: The mocked Session fixture.
    """
    # Arrange
    mock_session.return_value.__enter__.return_value.exec.return_value.all.return_value = [
        DBUser(id=1, username="testuser")
    ]

    # Act
    users = user_repository.read_all()

    # Assert
    assert len(users) == 1
    assert users[0].username == "testuser"


def test_create(user_repository, mock_session):
    """
    Test the create method of UserRepository.

    :param user_repository: The UserRepository instance.
    :param mock_session: The mocked Session fixture.
    """
    # Arrange
    user_create = UserCreate(
        username="testuser", email="test@example.com", password="testpassword"
    )
    mock_session.return_value.__enter__.return_value.commit.return_value = None
    mock_session.return_value.__enter__.return_value.refresh.return_value = None

    # Act
    created_user = user_repository.create(user_create)

    # Assert
    assert created_user.username == "testuser"
    assert created_user.email == "test@example.com"


def test_update(user_repository, mock_session):
    """
    Test the update method of UserRepository.

    :param user_repository: The UserRepository instance.
    :param mock_session: The mocked Session fixture.
    """
    # Arrange
    user_update = UserUpdate(
        username="updateduser", email="updated@example.com", password="hashed"
    )
    mock_session.return_value.__enter__.return_value.get.return_value = DBUser(
        id=1, username="testuser"
    )
    mock_session.return_value.__enter__.return_value.commit.return_value = None
    mock_session.return_value.__enter__.return_value.refresh.return_value = None

    # Act
    updated_user = user_repository.update(1, user_update)

    # Assert
    assert updated_user.username == "updateduser"
    assert updated_user.email == "updated@example.com"


def test_update_no_user(user_repository, mock_session):
    """
    Test the update method of UserRepository when the user does not exist.

    :param user_repository:
    :param mock_session:
    :return:
    """
    # Arrange
    user_update = UserUpdate(
        username="newuser", email="newuser@example.com", password="hashed"
    )
    expected_password_hash = get_password_hash(user_update.password)
    mock_session.return_value.__enter__.return_value.get.return_value = None
    mock_session.return_value.__enter__.return_value.commit.return_value = None
    mock_session.return_value.__enter__.return_value.refresh.return_value = None

    # Act
    updated_user = user_repository.update(1, user_update)

    # Assert
    assert updated_user is not None, "User should not be None"
    assert updated_user.id == 1, "User id should be 1"
    assert updated_user.username == "newuser", "User username should be newuser"
    assert (
        updated_user.email == "newuser@example.com"
    ), "User email should be newuser@example.com"
    assert verify_password(
        user_update.password, updated_user.hashed_password
    ), "Password should match"


def test_delete(user_repository, mock_session):
    """
    Test the delete method of UserRepository.

    :param user_repository: The UserRepository instance.
    :param mock_session: The mocked Session fixture.
    """
    # Arrange
    mock_session.return_value.__enter__.return_value.get.return_value = DBUser(
        id=1, username="testuser"
    )
    mock_session.return_value.__enter__.return_value.commit.return_value = None

    # Act
    result = user_repository.delete(1)

    # Assert
    assert result is True


def test_delete_no_user(user_repository, mock_session):
    """
    Test the delete method of UserRepository when the user does not exist.

    :param user_repository:
    :param mock_session:
    :return:
    """
    # Arrange
    mock_session.return_value.__enter__.return_value.get.return_value = None
    mock_session.return_value.__enter__.return_value.commit.return_value = None
    mock_session.return_value.__enter__.return_value.refresh.return_value = None

    # Act
    result = user_repository.delete(1)

    # Assert
    assert result is False, "Result should be False"
