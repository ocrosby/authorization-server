"""
This module contains the unit tests for the ClientRepository class.
"""

# tests/unit/app/repositories/test_client.py

import pytest
from app.models.client import DBClient
from app.repositories.client import ClientRepository
from app.schemas.client import Client


@pytest.fixture
def mock_session(mocker):
    """
    Fixture to mock the SQLModel Session.

    :param mocker: The pytest-mock mocker fixture.
    :return: Mocked Session.
    """
    return mocker.patch("app.repositories.client.Session", autospec=True)


@pytest.fixture
def client_repository(mock_session, mock_engine):
    """
    Fixture to create a ClientRepository instance with a mocked engine.

    :param mock_session: The mocked Session fixture.
    :return: ClientRepository instance.
    """
    return ClientRepository(mock_engine)


def test_read(client_repository, mock_session):
    """
    Test the read method of ClientRepository.

    :param client_repository: The ClientRepository instance.
    :param mock_session: The mocked Session fixture.
    """
    # Arrange
    mock_session_instance = mock_session.return_value.__enter__.return_value
    mock_session_instance.get.return_value = DBClient(id=1, client_name="testclient")

    # Act
    client = client_repository.read(1)

    # Assert
    assert client.id == 1
    assert client.client_name == "testclient"


def test_read_all(client_repository, mock_session):
    """
    Test the read_all method of ClientRepository.

    :param client_repository: The ClientRepository instance.
    :param mock_session: The mocked Session fixture.
    """
    # Arrange
    mock_session.return_value.__enter__.return_value.exec.return_value.all.return_value = [
        DBClient(id=1, client_name="testclient")
    ]

    # Act
    clients = client_repository.read_all()

    # Assert
    assert len(clients) == 1
    assert clients[0].client_name == "testclient"


def test_create(client_repository, mock_session):
    """
    Test the create method of ClientRepository.

    :param client_repository: The ClientRepository instance.
    :param mock_session: The mocked Session fixture.
    """
    # Arrange
    client_data = Client(
        client_id="123abc",
        client_secret="FFFFEEEE",
        client_name="testclient",
        redirect_uris=["http://localhost/callback"],
        grant_types=["authorization_code"],
        response_types=["code"],
        scope=["openid", "profile"],
    )
    mock_session.return_value.__enter__.return_value.commit.return_value = None
    mock_session.return_value.__enter__.return_value.refresh.return_value = None

    # Act
    created_client = client_repository.create(client_data)

    # Assert
    assert created_client.client_name == "testclient"


def test_update(client_repository, mock_session):
    """
    Test the update method of ClientRepository.

    :param client_repository: The ClientRepository instance.
    :param mock_session: The mocked Session fixture.
    """
    # Arrange
    client_data = Client(
        client_id="123abc",
        client_secret="FFFFEEEE",
        client_name="testclient",
        redirect_uris=["http://localhost/callback"],
        grant_types=["authorization_code"],
        response_types=["code"],
        scope=["openid", "profile"],
    )
    mock_session.return_value.__enter__.return_value.get.return_value = DBClient(
        id=1, client_name="testclient"
    )
    mock_session.return_value.__enter__.return_value.commit.return_value = None
    mock_session.return_value.__enter__.return_value.refresh.return_value = None

    # Act
    updated_client = client_repository.update(1, client_data)

    # Assert
    assert updated_client.client_name == "testclient"


def test_update_no_client(client_repository, mock_session):
    """
    Test the update method of ClientRepository when the client does not exist.

    :param client_repository:
    :param mock_session:
    :return:
    """
    # Arrange
    client_data = Client(
        client_id="123abc",
        client_secret="FFFFEEEE",
        client_name="testclient",
        redirect_uris=["http://localhost/callback"],
        grant_types=["authorization_code"],
        response_types=["code"],
        scope=["openid", "profile"],
    )
    mock_session.return_value.__enter__.return_value.get.return_value = None
    mock_session.return_value.__enter__.return_value.commit.return_value = None
    mock_session.return_value.__enter__.return_value.refresh.return_value = None

    # Act
    updated_client = client_repository.update(1, client_data)

    # Assert
    assert updated_client is not None, "Client should not be None"
    assert updated_client.id == 1, "Client id should be 1"
    assert (
        updated_client.client_name == "testclient"
    ), "Client client_name should be newclient"


def test_delete(client_repository, mock_session):
    """
    Test the delete method of ClientRepository.

    :param client_repository: The ClientRepository instance.
    :param mock_session: The mocked Session fixture.
    """
    # Arrange
    mock_session.return_value.__enter__.return_value.get.return_value = DBClient(
        id=1, client_name="testclient"
    )
    mock_session.return_value.__enter__.return_value.commit.return_value = None

    # Act
    result = client_repository.delete(1)

    # Assert
    assert result is True


def test_delete_no_client(client_repository, mock_session):
    """
    Test the delete method of ClientRepository when the client does not exist.

    :param client_repository:
    :param mock_session:
    :return:
    """
    # Arrange
    mock_session.return_value.__enter__.return_value.get.return_value = None
    mock_session.return_value.__enter__.return_value.commit.return_value = None
    mock_session.return_value.__enter__.return_value.refresh.return_value = None

    # Act
    result = client_repository.delete(1)

    # Assert
    assert result is False, "Result should be False"
