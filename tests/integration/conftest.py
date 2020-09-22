import pytest
from unittest.mock import Mock, MagicMock
import sqlite_utils
import regex as re
import os
import csv

DATA = "data/conversations.csv"

def row_generator(datafile):
    with open(datafile) as csvfile:
        readr = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in readr:
            if row == ["id", "name"]:
                meta = row
                continue
            yield {"id": row[0], "name": row[1]}
        #yield meta

"""populate a database for test"""
@pytest.fixture(scope="function", params=["c1", "c2", "c3"]) 
def mock_db(tmp_path_factory, request):

    db_dir = tmp_path_factory.mktemp("dbs")
    db_path = db_dir / "test_db.sqlite"
    db = sqlite_utils.Database(db_path)

    if request.param == "c1":
        datafile = "data/conversations.csv"
    elif request.param == "c2":
        datafile = "data/conversations_nonull.csv"
    elif request.param == "c3":
        datafile = "data/conversations_coalesced.csv"
    else:
        raise ValueError("Internal test config problem")
    
    pat = re.compile(r"(?<=/)[a-zA-Z]+")
    name_clean = pat.search(datafile).group()

    db[name_clean].insert_all(
        list(row_generator(datafile)), pk="id")
    return db

def db_data(param):
    if param == "c1":
        datafile = "data/conversations.csv"
    elif param == "c2":
        datafile = "data/conversations_nonull.csv"
    elif param == "c3":
        datafile = "data/conversations_coalesced.csv"
    else:
        raise ValueError("Internal test config problem")
    
    pat = re.compile(r"(?<=/)[a-zA-Z]+")
    name_clean = pat.search(datafile).group()
    return name_clean, list(row_generator(datafile))


#def pytest_generate_tests(metafunc):
  #  if "mock_db" in metafunc.fixturenames:
  #      metafunc.parametrize("mock_db", ["c1", "c2", "c3"], indirect=True)



class MockConn:
    def __init__(self, mock_db):
        self.mock_db = mock_db

    def execute(self, query):
        self.result = self.mock_db.execute("select id, name from conversations")

    def fetchall(self):
        return self.result.fetchall()

