import pytest
from fastapi import HTTPException, status
from jose import JWTError
from sqlmodel import Session, create_engine
from sqlalchemy.engine import Engine
from app.dependencies import (
    get_current_user,
    get_current_active_user,
    get_session,
    get_engine,
    get_client_repository,
    get_user_repository,
    get_client_service,
    get_user_service,
)
from app.models.token import TokenData
from app.models.user import DBUser
from app.repositories.client import ClientRepository
from app.repositories.user import UserRepository
from app.services.client import ClientService
from app.services.user import UserService
from app.utils import oauth2_scheme, get_user


@pytest.fixture
def mock_jwt(mocker):
    return mocker.patch("app.dependencies.jwt")


@pytest.fixture
def mock_db(mocker):
    return mocker.patch("app.dependencies.db")


@pytest.fixture
def mock_engine(mocker):
    return mocker.patch("app.dependencies.create_engine")


@pytest.fixture
def mock_session(mocker):
    return mocker.patch("app.dependencies.Session")


def test_get_current_user_valid_token(mock_jwt, mock_db):
    """
    Test get_current_user with a valid token.
    """
    # Arrange
    mock_jwt.decode.return_value = {"sub": "testuser"}
    mock_db.get_user.return_value = DBUser(
        id=1, username="testuser", hashed_password="hashed"
    )

    # Act
    user = get_current_user(token="valid_token")

    # Assert
    assert user.username == "testuser"
    mock_jwt.decode.assert_called_once_with(
        "valid_token", "SECRET_KEY", algorithms=["ALGORITHM"]
    )
    mock_db.get_user.assert_called_once_with(mock_db, username="testuser")


def test_get_current_user_invalid_token(mock_jwt):
    """
    Test get_current_user with an invalid token.
    """
    # Arrange
    mock_jwt.decode.side_effect = JWTError

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token="invalid_token")
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user_no_user(mock_jwt, mock_db):
    """
    Test get_current_user when the user is not found.
    """
    # Arrange
    mock_jwt.decode.return_value = {"sub": "testuser"}
    mock_db.get_user.return_value = None

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token="valid_token")
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_active_user_active():
    """
    Test get_current_active_user with an active user.
    """
    # Arrange
    current_user = DBUser(
        id=1, username="testuser", hashed_password="hashed", disabled=False
    )

    # Act
    user = get_current_active_user(current_user=current_user)

    # Assert
    assert user.username == "testuser"


def test_get_current_active_user_inactive():
    """
    Test get_current_active_user with an inactive user.
    """
    # Arrange
    current_user = DBUser(
        id=1, username="testuser", hashed_password="hashed", disabled=True
    )

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        get_current_active_user(current_user=current_user)
    assert exc_info.value.status_code == 400


def test_get_session(mock_session, mock_engine):
    """
    Test get_session function.
    """
    # Arrange
    mock_session.return_value.__enter__.return_value = "session"

    # Act
    session = next(get_session())

    # Assert
    assert session == "session"
    mock_session.assert_called_once()


def test_get_engine(mock_engine):
    """
    Test get_engine function.
    """
    # Arrange
    mock_engine.return_value = "engine"

    # Act
    engine = get_engine()

    # Assert
    assert engine == "engine"
    mock_engine.assert_called_once_with("sqlite:///./test.db")


def test_get_client_repository(mock_engine):
    """
    Test get_client_repository function.
    """
    # Arrange
    engine = "engine"

    # Act
    client_repository = get_client_repository(engine_obj=engine)

    # Assert
    assert isinstance(client_repository, ClientRepository)


def test_get_user_repository(mock_engine):
    """
    Test get_user_repository function.
    """
    # Arrange
    engine = "engine"

    # Act
    user_repository = get_user_repository(engine_obj=engine)

    # Assert
    assert isinstance(user_repository, UserRepository)


def test_get_client_service():
    """
    Test get_client_service function.
    """
    # Arrange
    client_repository = ClientRepository("engine")

    # Act
    client_service = get_client_service(client_repository=client_repository)

    # Assert
    assert isinstance(client_service, ClientService)


def test_get_user_service():
    """
    Test get_user_service function.
    """
    # Arrange
    user_repository = UserRepository("engine")

    # Act
    user_service = get_user_service(user_repository=user_repository)

    # Assert
    assert isinstance(user_service, UserService)
