import pytest
from utils import verify_password

from app.security import get_password_hash


@pytest.fixture
def mock_pwd_context(mocker):
    return mocker.patch("app.security.pwd_context")


def test_get_password_hash(mock_pwd_context):
    """
    Test the get_password_hash function.
    """
    # Arrange
    mock_pwd_context.hash.return_value = "hashed_password"

    # Act
    result = get_password_hash("plain_password")

    # Assert
    mock_pwd_context.hash.assert_called_once_with("plain_password")
