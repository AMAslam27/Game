import pytest


def test_plot_results_saves_percentages_and_creates_parent(plot_environment):
    plots, figure, canvases, paths = plot_environment
    saved = plots.plot_results(
        {1: 60, 0: 25, -1: 15}, "minimax", "random",
        output_path="results/chart.png",
    )
    assert saved is paths[0]
    assert paths[0].mkdir_calls == [{"parents": True, "exist_ok": True}]
    assert figure.saved == [(saved, {"dpi": 150})]
    assert canvases == [figure]
    labels, percentages, _ = figure.axes.bar_calls[0]
    assert labels == ["X wins\n(minimax)", "Draws", "O wins\n(random)"]
    assert percentages == pytest.approx([60, 25, 15])
    assert figure.axes.bar_label_calls[0][1]["labels"] == [
        "60 (60.0%)", "25 (25.0%)", "15 (15.0%)",
    ]
    assert figure.cleared


def test_plot_results_skips_empty_run(plot_environment):
    plots, figure, canvases, paths = plot_environment
    assert plots.plot_results({1: 0, 0: 0, -1: 0}, "x", "o", output_path="unused.png") is None
    assert not canvases
    assert not paths
    assert not figure.saved


@pytest.mark.parametrize("outcome", [1, 0, -1])
def test_plot_results_rejects_negative_counts(plot_environment, outcome):
    plots, figure, canvases, paths = plot_environment
    results = {1: 0, 0: 0, -1: 0}
    results[outcome] = -1
    with pytest.raises(ValueError, match="negative"):
        plots.plot_results(results, "x", "o", output_path="unused.png")
    assert not paths
    assert not canvases
    assert not figure.saved


def test_plot_results_cleans_up_when_save_fails(plot_environment):
    plots, figure, _, _ = plot_environment
    figure.save_error = OSError("Unable to save")
    with pytest.raises(OSError, match="Unable to save"):
        plots.plot_results({1: 1, 0: 0, -1: 0}, "x", "o", output_path="chart.png")
    assert len(figure.saved) == 1
    assert figure.cleared
