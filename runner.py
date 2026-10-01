"""Entry point for running TicTacToe games.

Examples:
    python runner.py                          # human vs human
    python runner.py --x human --o random     # you (X) vs random bot
    python runner.py --x random --o random --games 1000 --quiet
"""

import argparse

from games.tictactoe.play import human_policy, play_game, random_policy
from games.tictactoe.rules import EMPTY, PLAYER_O, PLAYER_X
from players.minimax import minimax_policy

# Register new players here (e.g. a trained agent) to make them selectable.
POLICIES = {
    "human": human_policy,
    "random": random_policy,
    "minimax": minimax_policy
}


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
        help="save the results chart to this path",
    )
    return parser.parse_args()

def print_progress(completed, total):
    if completed % 100 == 0 or completed == total:
        print(f"{completed}/{total} games completed", flush=True)

def print_summary(results):
    total = sum(results.values())
    print(f"\nResults over {total} game(s):")
    print(f"  X wins: {results[PLAYER_X]}")
    print(f"  O wins: {results[PLAYER_O]}")
    print(f"  Draws:  {results[EMPTY]}")


def main():
    args = parse_args()
    policy_x, policy_o = POLICIES[args.x], POLICIES[args.o]
    interactive = "human" in (args.x, args.o)
    results = {PLAYER_X: 0, PLAYER_O: 0, EMPTY: 0}

    if not args.quiet:
        print(f"X: {args.x} | O: {args.o}. Squares are numbered 1-9.")

    while True:
        quit_early = False
        for game_number in range(1, args.games + 1):
            winner = play_game(policy_x, policy_o, verbose=not args.quiet)
            if winner is None:
                quit_early = True
                break

            results[winner] += 1

            if args.games > 1:
                print_progress(game_number, args.games)

        if quit_early or not interactive:
            break
        again = input("Play again? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            break

    if args.games > 1 or args.quiet or sum(results.values()) > 1:
        print_summary(results)

    if args.plot_file:
        from evaluation.plots import plot_results

        saved_path = plot_results(
            results,
            args.x,
            args.o,
            output_path=args.plot_file,
        )

        if saved_path is not None:
            print(f"Chart saved to: {saved_path}")


if __name__ == "__main__":
    main()
