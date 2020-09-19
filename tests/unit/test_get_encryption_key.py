import pytest
from pytest import raises
from unittest.mock import MagicMock

from signal_desktop_backup.signal_desktop_backup import get_encryption_key

FAKE_KEY = {"key": "c272eba221c438478166696c82a270e7ec9e63821469d215016a6dcc429d46b1"}


@pytest.fixture()
def mock_open(monkeypatch):
    mock_file = MagicMock()
    mock_file.read = MagicMock()
    mock_file.read.return_value = FAKE_KEY
    mock_open = MagicMock(return_value=mock_file)
    monkeypatch.setattr("builtins.open", mock_open)
    return mock_open


def test_returnsCorrectKey(mock_open, monkeypatch):
    mock_exists = MagicMock(return_value=True)
    monkeypatch.setattr("os.path.exists", mock_exists)
    monkeypatch.setattr("json.loads", mock_open.return_value.read)
    result = get_encryption_key("config.json")
    mock_open.assert_called_once_with("config.json", "r")
    assert result == FAKE_KEY["key"]


def test_raiseExceptionIfNotExistsFile(mock_open, monkeypatch):
    mock_exists = MagicMock(return_value=False)
    monkeypatch.setattr("os.path.exists", mock_exists)
    with raises(Exception):
        _ = get_encryption_key("config.json")


def test_raiseExceptionIfNotExistsKey(mock_open, monkeypatch):
    mock_exists = MagicMock(return_value=True)
    monkeypatch.setattr("os.path.exists", mock_exists)
    monkeypatch.setattr("json.loads", mock_open.return_value.read)
    monkeypatch.delitem(mock_open.return_value.read.return_value, "key", raising=True)

    with raises(KeyError):
        _ = get_encryption_key("config.json")
