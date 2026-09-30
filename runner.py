"""Entry point for running TicTacToe games.

Examples:
    python runner.py                          # human vs human
    python runner.py --x human --o random     # you (X) vs random bot
    python runner.py --x random --o random --games 1000 --quiet
"""
import argparse

from games.tictactoe.play import play_game, human_policy, random_policy, NAMES
from games.tictactoe.rules import PLAYER_X, PLAYER_O, EMPTY

# Register new players here (e.g. a trained agent) to make them selectable.
POLICIES = {
    "human": human_policy,
    "random": random_policy,
}


def parse_args():
    parser = argparse.ArgumentParser(description="Run TicTacToe games.")
    parser.add_argument("--x", choices=POLICIES, default="human", help="player X (moves first)")
    parser.add_argument("--o", choices=POLICIES, default="human", help="player O")
    parser.add_argument("--games", type=int, default=1, help="number of games to play")
    parser.add_argument("--quiet", action="store_true", help="don't print boards or per-game results")
    return parser.parse_args()


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
        for _ in range(args.games):
            winner = play_game(policy_x, policy_o, verbose=not args.quiet)
            if winner is None:  # a human quit
                quit_early = True
                break
            results[winner] += 1

        if quit_early or not interactive:
            break
        again = input("Play again? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            break

    if args.games > 1 or args.quiet or sum(results.values()) > 1:
        print_summary(results)


if __name__ == "__main__":
    main()