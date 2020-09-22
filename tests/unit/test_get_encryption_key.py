import pytest
from pytest import raises
from unittest.mock import MagicMock

import os
import json

from signal_desktop_backup.signal_desktop_backup import EncryptionKey

FAKE_KEY = {"key": "c272eba221c438478166696c82a270e7ec9e63821469d215016a6dcc429d46b1"}


class MockJson:

    @staticmethod
    def loads(*args, **kwargs):
        return FAKE_KEY

@pytest.fixture()
def mock_open(monkeypatch):

    def mock_json(*args, **kwargs):
        return MockJson().loads()

    mock_open = MagicMock(read_data=FAKE_KEY)
    monkeypatch.setattr("builtins.open", mock_open)
    monkeypatch.setattr("json.loads", mock_json)
    return mock_open


def test_returnsCorrectKey(mock_open, monkeypatch):
    mock_exists = MagicMock(return_value=True)
    monkeypatch.setattr("os.path.exists", lambda: mock_exists)
    ek = EncryptionKey()
    result = ek.get_encryption_key("config.json")
    mock_open.assert_called_once_with("config.json", "r")
    assert result == FAKE_KEY["key"]


def test_raiseExceptionIfNotExistsFile(mock_open, monkeypatch):
    mock_open.side_effect = FileNotFoundError()
    with raises(FileNotFoundError) as excinfo:
        ek = EncryptionKey()
        _ = ek.get_encryption_key("config.json")

        print(excinfo)


def test_raiseExceptionIfNotExistsKey(mock_open, monkeypatch):
    mock_exists = MagicMock(return_value=True)
    monkeypatch.setattr("os.path.exists", mock_exists)
    monkeypatch.setattr("json.loads", lambda x: {})

    with raises(KeyError, match="key") as excinfo:
        ek = EncryptionKey()
        _ = ek.get_encryption_key("config.json")