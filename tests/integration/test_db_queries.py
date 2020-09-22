import pytest
import re
from unittest.mock import Mock, MagicMock, patch
from signal_desktop_backup.signal_desktop_backup import get_conversations
from sqlcipher3 import dbapi2


def test_get_conversationsIdsOk(monkeypatch, mock_db):

    for id_, name_ in get_conversations(mock_db):
        assert re.match(r"([a-f0-9]+-){4}([a-f0-9]+)", id_)


def test_get_conversationsNamesOk(monkeypatch, mock_db):
    """
    Expected to fail on original inputs because the `conversation`
    table permits null values in the `name` column.
    """
    for id_, name_ in get_conversations(mock_db):
        assert len(name_) > 0
        assert name_ is not None
