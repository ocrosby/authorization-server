"""
This module contains tests for the client service.
"""

import pytest

from app.models.client import DBClient
from app.repositories.client import ClientRepository
from app.schemas.client import ClientCreate, ClientUpdate
from app.services.client import ClientService


@pytest.fixture
def mock_repository(mocker):
    """
    Create a mock client repository

    :param mocker:
    :return:
    """
    return mocker.Mock()


@pytest.fixture
def client_service(mock_repository: ClientRepository) -> ClientService:
    """
    This fixture creates a client service

    :param mock_repository:
    :return:
    """
    return ClientService(mock_repository)


@pytest.fixture
def mock_db_client(mocker):
    """
    This fixture creates a mock client

    :param mocker:
    :return:
    """
    mock_client = mocker.Mock()

    mock_client.client_id = "newclient"
    mock_client.client_secret = "newclientsecret"

    return mock_client


@pytest.fixture
def test_db_client():
    """
    This fixture creates a test client

    :return:
    """
    return DBClient(
        client_id="newclient",
        client_secret="newclientsecret",
        client_name="New Client",
        client_uri="https://example.com",
        logo_uri="https://example.com/logo.png",
        redirect_uris=["https://example.com/callback"],
        default_scopes=["openid", "profile"],
        response_types=["code"],
        grant_types=["authorization_code"],
        token_endpoint_auth_method="client_secret_basic",
    )


@pytest.fixture
def client_create():
    """
    This fixture creates a test client create schema

    :return:
    """
    return ClientCreate(
        client_id="newclient",
        client_secret="newclientsecret",
        client_name="New Client",
        client_uri="https://example.com",
        logo_uri="https://example.com/logo.png",
        redirect_uris=["https://example.com/callback"],
        scope=["openid", "profile"],
        response_types=["code"],
        grant_types=["authorization_code"],
    )


@pytest.fixture
def client_update():
    """
    This fixture creates a test client update schema

    :return:
    """
    return ClientUpdate(
        client_id="newclient",
        client_secret="newclientsecret",
        client_name="New Client",
        client_uri="https://example.com",
        logo_uri="https://example.com/logo.png",
        redirect_uris=["https://example.com/callback"],
        scope=["openid", "profile"],
        response_types=["code"],
        grant_types=["authorization_code"],
    )


def test_create(mock_repository, client_create, client_service, mock_db_client) -> None:
    """
    This function tests the create method of the client service.

    :param mock_repository:
    :param client_create:
    :param client_service:
    :param mock_db_client:
    :return:
    """
    # Arrange
    mock_repository.create.return_value = mock_db_client

    # Act
    result = client_service.create(client_create)

    # Assert
    assert result == mock_db_client
    mock_repository.create.assert_called_once_with(client_create)


def test_read(mock_repository, client_service, mock_db_client) -> None:
    """
    This function tests the read method of the client service.

    :param mock_repository:
    :param client_service:
    :param mock_db_client:
    :return:
    """
    # Arrange
    mock_repository.read.return_value = mock_db_client

    # Act
    result = client_service.read(1)

    # Assert
    assert result == mock_db_client
    mock_repository.read.assert_called_once_with(1)


def test_update(mock_repository, client_update, client_service, mock_db_client) -> None:
    """
    This function tests the update method of the client service.

    :param mock_repository:
    :param client_update:
    :param client_service:
    :param mock_db_client:
    :return:
    """
    # Arrange
    mock_repository.update.return_value = mock_db_client

    # Act
    result = client_service.update(1, client_update)

    # Assert
    assert result == mock_db_client
    mock_repository.update.assert_called_once_with(1, client_update)


def test_delete(mock_repository, client_service) -> None:
    """
    This function tests the delete method of the client service.

    :param mock_repository:
    :param client_service:
    :return:
    """
    # Arrange
    mock_repository.delete.return_value = True

    # Act
    result = client_service.delete(1)

    # Assert
    assert result is True
    mock_repository.delete.assert_called_once_with(1)
