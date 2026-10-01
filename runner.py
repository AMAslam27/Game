"""Entry point for running TicTacToe games.

Examples:
    python runner.py                          # human vs human
    python runner.py --x human --o random     # you (X) vs random bot
    python runner.py --x random --o random --games 1000 --quiet
"""

import argparse
import logging
import random
from contextlib import closing
from pathlib import Path

from evaluation.artifacts import save_run_plot
from evaluation.database import DEFAULT_DB_PATH, connect_database
from evaluation.recorder import RunRecorder
from games.tictactoe.play import human_policy, play_game, random_policy
from games.tictactoe.rules import EMPTY, PLAYER_O, PLAYER_X
from players.minimax import minimax_policy

logger = logging.getLogger(__name__)

# Register new players here (e.g. a trained agent) to make them selectable.
POLICIES = {"human": human_policy, "random": random_policy, "minimax": minimax_policy}


def parse_args():
    parser = argparse.ArgumentParser(description="Run TicTacToe games.")
    parser.add_argument(
        "--x", choices=POLICIES, default="human", help="player X (moves first)"
    )
    parser.add_argument("--o", choices=POLICIES, default="human", help="player O")
    parser.add_argument("--games", type=int, default=1, help="number of games to play")
    parser.add_argument(
        "--quiet", action="store_true", help="don't print boards or per-game results"
    )
    parser.add_argument(
        "--plot-file",
        help="override the automatic timestamped chart path",
    )
    parser.add_argument(
        "--db-file",
        type=Path,
        default=DEFAULT_DB_PATH,
        help="SQLite results database (default: project results/games.sqlite3)",
    )
    parser.add_argument("--seed", type=int, help="random seed for each game batch")
    args = parser.parse_args()
    if args.games <= 0:
        parser.error("--games must be a positive integer")
    return args


def print_progress(completed, total):
    if completed % 100 == 0 or completed == total:
        print(f"{completed}/{total} games completed", flush=True)


def print_summary(results):
    total = sum(results.values())
    print(f"\nResults over {total} game(s):")
    print(f"  X wins: {results[PLAYER_X]}")
    print(f"  O wins: {results[PLAYER_O]}")
    print(f"  Draws:  {results[EMPTY]}")


def finish_after_error(recorder, status):
    """Try to preserve the final status without hiding the original error."""
    try:
        recorder.finish_run(status)
    except Exception:
        logger.exception("Could not save status for run %s", recorder.run_id)


def main():
    args = parse_args()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    policy_x, policy_o = POLICIES[args.x], POLICIES[args.o]
    interactive = "human" in (args.x, args.o)
    results = {PLAYER_X: 0, PLAYER_O: 0, EMPTY: 0}

    if not args.quiet:
        print(f"X: {args.x} | O: {args.o}. Squares are numbered 1-9.")

    with closing(connect_database(args.db_file)) as connection:
        batch_number = 0
        while True:
            batch_number += 1
            batch_results = {PLAYER_X: 0, PLAYER_O: 0, EMPTY: 0}
            recorder = RunRecorder(connection)
            if args.seed is not None:
                random.seed(args.seed)
            run_id = recorder.start_run(args.x, args.o, args.games, seed=args.seed)
            logger.info(
                "Started run %s: X=%s, O=%s, games=%s",
                run_id,
                args.x,
                args.o,
                args.games,
            )

            try:
                quit_early = False
                for game_number in range(1, args.games + 1):
                    winner = play_game(policy_x, policy_o, verbose=not args.quiet)
                    if winner is None:
                        quit_early = True
                        break

                    recorder.record_game(game_number, winner)
                    results[winner] += 1
                    batch_results[winner] += 1
                    if args.games > 1:
                        print_progress(game_number, args.games)

                status = "abandoned" if quit_early else "completed"
                recorder.finish_run(status)
                logger.info("Finished run %s: %s", run_id, status)
            except KeyboardInterrupt:
                finish_after_error(recorder, "interrupted")
                logger.warning("Run %s interrupted", run_id)
                raise
            except Exception:
                finish_after_error(recorder, "failed")
                logger.exception("Run %s failed", run_id)
                raise

            output_path = args.plot_file
            if output_path is not None and batch_number > 1:
                path = Path(output_path)
                output_path = path.with_name(f"{path.stem}_run-{run_id}{path.suffix}")
            saved_path = save_run_plot(
                batch_results, args.x, args.o, recorder, output_path=output_path
            )
            if saved_path is not None:
                print(f"Chart saved to: {saved_path}")

            if quit_early or not interactive:
                break
            again = input("Play again? (y/n): ").strip().lower()
            if again not in ("y", "yes"):
                break

    if args.games > 1 or args.quiet or sum(results.values()) > 1:
        print_summary(results)


if __name__ == "__main__":
    main()
