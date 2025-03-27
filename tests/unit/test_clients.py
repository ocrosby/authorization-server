"""
This module tests the API routes for clients.
"""
import pytest

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)



def test_create_client(mock_db_session):
    """
    This function tests the create_client route

    :param mock_db_session:
    :return:
    """
    # Arrange
    new_client = {
        "client_id": "example_client_id",
        "client_secret": "example_client_secret",
        "redirect_uris": ["https://example.com/callback"],
        "grant_types": ["authorization_code"],
        "response_types": ["code"],
        "client_name": "Example Client",
        "client_uri": "https://example.com",
        "logo_uri": "https://example.com/logo.png",
        "scope": ["read", "write"],
        "contacts": ["contact@example.com"],
        "tos_uri": "https://example.com/tos",
        "policy_uri": "https://example.com/policy"
    }

    # Act
    response = client.post(
        url="/clients/",
        json=new_client
    )

    # Assert
    data = response.json()

    assert response.status_code == 201, f"Failed with response: {data}"
    assert data["client_id"] == new_client["client_id"]
    assert data["client_secret"] == new_client["client_secret"]
    assert data["redirect_uris"] == new_client["redirect_uris"]
    assert data["grant_types"] == new_client["grant_types"]
    assert data["response_types"] == new_client["response_types"]
    assert data["client_name"] == new_client["client_name"]
    assert data["client_uri"] == new_client["client_uri"]
    assert data["logo_uri"] == new_client["logo_uri"]
    assert data["scope"] == new_client["scope"]
    assert data["contacts"] == new_client["contacts"]
    assert data["tos_uri"] == new_client["tos_uri"]
    assert data["policy_uri"] == new_client["policy_uri"]

    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()

