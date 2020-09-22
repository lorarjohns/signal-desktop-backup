import pytest
from pytest import raises
from unittest.mock import (
    MagicMock,
    mock_open,
    patch
)
import io

import os
import json

from signal_desktop_backup.signal_desktop_backup import EncryptionKey

FAKE_KEY = {"key": "c272eba221c438478166696c82a270e7ec9e63821469d215016a6dcc429d46b1"}


def test_returnsCorrectKey(monkeypatch):
    mock_o = mock_open(read_data=json.dumps(FAKE_KEY))
    with patch("builtins.open", mock_o):
        with patch("json.loads", return_value=FAKE_KEY) as mock_loads:
            ek = EncryptionKey()
            result = ek.get_encryption_key("config.json")
            mock_o.assert_called_with("config.json", "r")
            mock_loads.assert_called_once_with(json.dumps(FAKE_KEY))
            assert result == FAKE_KEY["key"]


def test_raiseExceptionIfNotExistsFile(monkeypatch):
    mock_o = MagicMock(side_effect=FileNotFoundError)
    monkeypatch.setattr("builtins.open", mock_o)
    with raises(FileNotFoundError, match="Config file does not exist"):
        ek = EncryptionKey()
        assert ek.get_encryption_key("notafile")
        assert mock_o.called_once_with("notafile", "r")


def test_raiseExceptionIfNotExistsKey(monkeypatch):
    mock_o = mock_open()
    with raises(KeyError, match="Encryption key is missing from config file"):
        with patch("builtins.open", mock_o):
            with patch("json.loads", return_value={}):
                ek = EncryptionKey()
                assert ek.get_encryption_key("config.json")
                mock_o.assert_called_once_with("config.json", "r")  # TODO wrong number
