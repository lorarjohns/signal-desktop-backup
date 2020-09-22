import pytest
from unittest.mock import Mock, MagicMock
import os
from signal_desktop_backup.signal_desktop_backup import SQLCipherConnection

from sqlcipher3 import dbapi2 as sqlite

@pytest.fixture(scope='function')
def reset_sqlite_db(request):
    path = request.param  # Path to database file
    with open(path, 'w'): 
        pass
    yield None
    os.remove(path)

@pytest.mark.parametrize('reset_sqlite_db', ['/tmp/test_db.sql'], indirect=True)
def test_send_message(reset_sqlite_db):
    pass

def test_create_file(tmpdir):
    p = tmpdir.mkdir("sub").join("hello.txt")
    p.write("Hello")
    assert p.read() == "Hello"
    assert len(tmpdir.listdir()) == 1
