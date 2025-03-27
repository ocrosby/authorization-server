"""
This file contains the fixtures that are used in the unit tests
"""

import pytest

@pytest.fixture
def mock_db_session(mocker):
    """
    This function mocks the database session

    :param mocker:
    :return:
    """
    mock_session = mocker.Mock()
    mocker.patch("app.dependencies.get_session", return_value=mock_session)
    return mock_session
