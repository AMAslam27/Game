"""Record one batch of games with a transaction per completed game."""

from datetime import UTC, datetime


def utc_timestamp():
    return datetime.now(UTC).isoformat()


class RunRecorder:
    def __init__(self, connection):
        self.connection = connection
        self.run_id: int | None = None
        self.finished = False
        self.started_at: str | None = None

    def start_run(self, policy_x, policy_o, requested_games, seed=None):
        if self.run_id is not None:
            raise ValueError("This recorder has already started a run")
        if requested_games <= 0:
            raise ValueError("Requested games must be positive")

        started_at = utc_timestamp()
        with self.connection:
            cursor = self.connection.execute(
                """
                INSERT INTO runs (
                    started_at, policy_x, policy_o, requested_games, seed
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (started_at, policy_x, policy_o, requested_games, seed),
            )
            run_id = cursor.lastrowid
            if run_id is None:
                raise RuntimeError("Database did not return a run ID")

        self.started_at = started_at
        self.run_id = run_id
        return run_id

    def record_game(self, game_number, winner):
        self._require_active_run()
        if game_number <= 0:
            raise ValueError("Game number must be positive")
        if winner not in (-1, 0, 1):
            raise ValueError("Winner must be -1, 0, or 1")
        with self.connection:
            self.connection.execute(
                """
                INSERT INTO games (run_id, game_number, winner)
                VALUES (?, ?, ?)
                """,
                (self.run_id, game_number, winner),
            )

    def finish_run(self, status="completed"):
        self._require_active_run()
        if status not in {"completed", "abandoned", "interrupted", "failed"}:
            raise ValueError(f"Invalid final status: {status}")
        with self.connection:
            self.connection.execute(
                """
                UPDATE runs SET finished_at = ?, status = ? WHERE id = ?
                """,
                (utc_timestamp(), status, self.run_id),
            )
        self.finished = True

    def _require_active_run(self):
        if self.run_id is None:
            raise ValueError("Start a run before recording results")
        if self.finished:
            raise ValueError("This run has already finished")
