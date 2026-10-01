import importlib
import sys
from types import ModuleType

import pytest

from tests.unit_tests.common.mock_utils import FakeFigure, FakePath


@pytest.fixture
def plot_environment(monkeypatch):
    figure = FakeFigure()
    canvases = []
    paths = []

    def figure_factory(**kwargs):
        return figure

    def path_factory(path):
        result = FakePath(path)
        paths.append(result)
        return result

    # Replace the plotting dependencies before importing the unit under test.
    # Tests need neither Matplotlib rendering nor a real filesystem.
    matplotlib = ModuleType("matplotlib")
    matplotlib.__path__ = []
    backends = ModuleType("matplotlib.backends")
    backends.__path__ = []
    agg = ModuleType("matplotlib.backends.backend_agg")
    agg.FigureCanvasAgg = canvases.append
    figures = ModuleType("matplotlib.figure")
    figures.Figure = figure_factory
    for name, module in {
        "matplotlib": matplotlib,
        "matplotlib.backends": backends,
        "matplotlib.backends.backend_agg": agg,
        "matplotlib.figure": figures,
    }.items():
        monkeypatch.setitem(sys.modules, name, module)

    monkeypatch.delitem(sys.modules, "evaluation.plots", raising=False)
    import evaluation
    monkeypatch.delattr(evaluation, "plots", raising=False)
    plots = importlib.import_module("evaluation.plots")
    # Register restoration of the newly imported fake-backed module as well.
    del sys.modules["evaluation.plots"]
    monkeypatch.setitem(sys.modules, "evaluation.plots", plots)
    del evaluation.plots
    monkeypatch.setattr(evaluation, "plots", plots, raising=False)
    monkeypatch.setattr(plots, "Path", path_factory)
    return plots, figure, canvases, paths
