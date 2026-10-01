import pytest

from evaluation import database
from tests.unit_tests.common.mock_utils import FakePath


@pytest.fixture
def database_environment(monkeypatch, fake_connection):
    path = FakePath("results/games.sqlite3")
    connections = []

    def fake_connect(value):
        connections.append(value)
        return fake_connection

    monkeypatch.setattr(database, "Path", lambda value: path)
    monkeypatch.setattr(database.sqlite3, "connect", fake_connect)
    return path, connections


def test_connect_database_initialises_schema_and_foreign_keys(database_environment, fake_connection):
    path, connections = database_environment
    assert database.connect_database("results/games.sqlite3") is fake_connection
    assert connections == [path]
    assert path.mkdir_calls == [{"parents": True, "exist_ok": True}]
    assert fake_connection.executions == [("PRAGMA foreign_keys = ON", ())]
    assert fake_connection.scripts == [database.SCHEMA]
    assert not fake_connection.closed


def test_connect_database_closes_connection_on_setup_failure(database_environment, fake_connection):
    fake_connection.error = OSError("Setup failed")
    with pytest.raises(OSError, match="Setup failed"):
        database.connect_database("results/games.sqlite3")
    assert fake_connection.closed
