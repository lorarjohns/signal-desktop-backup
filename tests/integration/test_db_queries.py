import pytest
import re
from unittest.mock import Mock, MagicMock, patch
from signal_desktop_backup.signal_desktop_backup import get_conversations
from sqlcipher3 import dbapi2


def test_get_conversationsIdsOk(monkeypatch, mock_db):

    for id_, name_ in get_conversations(mock_db):
        assert re.match(r"([a-f0-9]+-){4}([a-f0-9]+)", id_)
        print(id_)

@pytest.mark.xfail
def test_get_conversationsNamesOk(monkeypatch, mock_db):
    """
    Expected to fail on original inputs because the `conversation`
    table permits null values in the `name` column.
    """
    for id_, name_ in get_conversations(mock_db):
        assert len(name_) > 0


'''
The c3 test represents coalescing `name` and `e164` (phone number)
to achieve conversation identifiers 
query = "select id, coalesce(name, e164) as nonNullName from conversations"
'''
def test_get_conversationsNamesNumsCoalesced(monkeypatch, mock_db):

    for id_, name_ in get_conversations(mock_db):
        pass