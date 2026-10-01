from evaluation.artifacts import default_plot_path
from evaluation.database import PROJECT_ROOT


def test_default_plot_path_contains_utc_timestamp_and_run_id():
    path = default_plot_path(42, "2026-10-01T13:30:25.123456+01:00")
    assert path == PROJECT_ROOT / "results/tictactoe/plots/20261001T123025123456Z_run-42.png"


def test_default_plot_path_distinguishes_run_ids():
    timestamp = "2026-10-01T12:00:00+00:00"
    assert default_plot_path(1, timestamp) != default_plot_path(2, timestamp)


def test_default_plot_path_supports_other_game_directories():
    path = default_plot_path(7, "2026-10-01T12:00:00+00:00", game="connect4")
    assert path.parent == PROJECT_ROOT / "results/connect4/plots"
