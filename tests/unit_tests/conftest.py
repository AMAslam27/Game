import pytest

import runner
from evaluation import artifacts
from tests.unit_tests.common.mock_utils import FakeConnection, FakePlotter


@pytest.fixture
def fake_connection():
    return FakeConnection()


@pytest.fixture(autouse=True)
def isolate_runner_database(monkeypatch, fake_connection):
    monkeypatch.setattr(runner, "connect_database", lambda path: fake_connection)


@pytest.fixture(autouse=True)
def isolate_runner_plotting(monkeypatch):
    plotter = FakePlotter()
    monkeypatch.setattr(artifacts, "plot_results", plotter)
    return plotter
