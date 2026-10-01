"""Build portable chart filenames from recorded run metadata."""

from datetime import UTC, datetime
from pathlib import Path

from evaluation.database import PROJECT_ROOT
from evaluation.plots import plot_results


def default_plot_path(run_id, started_at, game="tictactoe"):
    timestamp = datetime.fromisoformat(started_at).astimezone(UTC)
    stamp = timestamp.strftime("%Y%m%dT%H%M%S%fZ")
    return PROJECT_ROOT / "results" / game / "plots" / f"{stamp}_run-{run_id}.png"


def save_run_plot(results, policy_x, policy_o, recorder, output_path=None):
    path = (
        Path(output_path)
        if output_path is not None
        else default_plot_path(recorder.run_id, recorder.started_at)
    )
    return plot_results(results, policy_x, policy_o, output_path=path)
