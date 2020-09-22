import pytest
from unittest.mock import Mock, MagicMock
import sqlite_utils
from sqlcipher3 import dbapi2 as sqlite

import regex as re
import os
import csv


def row_generator(datafile):
    with open(datafile) as csvfile:
        keys = None  # ("id", "name", "e164")
        readr = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in readr:
            if row == ["id", "name", "e164"]:
                meta = row
                keys = meta
                continue
            yield _normalize_nulls(row, keys)


def _normalize_nulls(row, keys):
    """
    Keep python/sqlite3 from turning legitimate Nulls
    into empty strings (which are not Null) when
    loading data from csv.
    """
    row = map(lambda x: None if x == "" else x, row)
    return {k: v for k, v in zip(keys, row)}

"""populate a database for test"""
@pytest.fixture(scope="session") 
def mock_db(tmp_path_factory):

    db_dir = tmp_path_factory.mktemp("dbs")
    db_path = db_dir / "test_db.sqlite"
    db = sqlite_utils.Database(db_path)

    datafile = "data/raw-conversations.csv"
    
    # pat = re.compile(r"(?<=/)[a-zA-Z]+")
    # name_clean = pat.search(datafile).group()

    db["conversations"].insert_all(
        list(row_generator(datafile)), pk="id")
    return db


class MockConn:
    def __init__(self, mock_db):
        self.mock_db = mock_db

    def execute(self, query):
        self.result = self.mock_db.execute("select id, name from conversations")

    def fetchall(self):
        return self.result.fetchall()

