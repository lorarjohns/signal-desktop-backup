import pytest
from unittest.mock import Mock, MagicMock

# mock db


@pytest.fixture()
def mock_database():
    mock_data = MagicMock()
    mock_conn = MagicMock()
    mock_conn.get_connection = MagicMock()
    mock_conn.get_connection.return_value = mock_data


@pytest.fixture()
def mock_key():
    pass


# mock os
