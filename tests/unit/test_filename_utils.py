#!/usr/bin/env python3

import pytest
import unicodedata
import regex

from signal_desktop_backup.signal_desktop_backup import _get_valid_filename, _replace_unicode

def test_get_valid_filename(conversation):
    observed = _get_valid_filename(conversation.original)
    assert observed == conversation.expected