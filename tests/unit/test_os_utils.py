import pytest
from unittest.mock import Mock, MagicMock

FAKE_TIMESTAMP = "20202109/19/20_152135"
FAKE_DIRNAME = "/Users/me"
FAKE_CWD = FAKE_DIRNAME + "/signal-desktop-backup"


@pytest.fixture()
def mock_os():
    mock_os = MagicMock()
    mock_os.getcwd.return_value = FAKE_CWD
    mock_os.path = MagicMock()
    mock_os.path.join = MagicMock()
    mock_os.path.abspath = MagicMock(return_value=FAKE_CWD + "/templates")
    mock_os.path.dirname = MagicMock(return_value=FAKE_DIRNAME)
    return mock_os


@pytest.fixture()
def mock_copyfile():
    mock_copyfile = MagicMock()
    return mock_copyfile


def test_create_output_directory(mock_os, mock_copyfile, monkeypatch):
    monkeypatch.setattr("time.strftime", "20202109/19/20_152135")

    fake_output_dir = FAKE_CWD + f"/signal_export_{FAKE_TIMESTAMP}"
    assert mock_os.path.join.called_with(FAKE_CWD, f"signal_export_{FAKE_TIMESTAMP}")
    assert mock_os.mkdir.called_with(fake_output_dir)
    assert mock_os.mkdir.called_with(fake_output_dir + "/conversations")
    assert mock_os.path.join.called_with(
        mock_os.path.dirname.return_value, "templates", "style.css"
    )
    assert mock_os.path.abspath.called_once()
    assert mock_os.path.join.called_with(fake_output_dir, "style.css")
    assert mock_copyfile.called_with(
        FAKE_DIRNAME + "/templates/style.css", fake_output_dir + "/style.css"
    )
