#!/usr/bin/env python3

import pytest
from unittest.mock import Mock, MagicMock

from signal_desktop_backup.signal_desktop_backup import (
    _get_valid_filename,
    _hash_name,
    get_conversation_filename
)


def test_get_valid_filename(conversation):
    observed = _get_valid_filename(conversation.original)
    assert observed == conversation.expected


def test_hash_name(conversation):
    observed = _get_valid_filename(conversation.original)
    observed_hash = _hash_name(observed)

    assert observed_hash == conversation.hash


def test_get_conversation_filename(conversation):
    observed = get_conversation_filename(conversation.original)
    expected = f"{conversation.expected}_{conversation.hash}.html"

    assert observed == expected