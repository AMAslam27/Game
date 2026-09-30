"""Reusable play functions for TicTacToe. No entry point here; see runner.py.

A *policy* is any callable: policy(game) -> action (0-8), or None to quit.
"""

import random

from .rules import EMPTY, PLAYER_O, PLAYER_X, TicTacToe

NAMES = {PLAYER_X: "X", PLAYER_O: "O"}


def show_board(game):
    """Print the board; empty squares show their number (1-9) as a hint."""
    cells = [NAMES[v] if v != EMPTY else str(i + 1) for i, v in enumerate(game.board)]
    print()
    for r in range(3):
        print(" " + " | ".join(cells[r * 3 : r * 3 + 3]))
        if r < 2:
            print("---+---+---")
    print()


def human_policy(game):
    """Prompt until a legal square (1-9) is entered. Returns None on quit."""
    legal = game.legal_actions()
    name = NAMES[game.current_player]
    while True:
        text = (
            input(f"Player {name}, choose a square (1-9, or 'q' to quit): ")
            .strip()
            .lower()
        )
        if text in ("q", "quit"):
            return None
        if not text.isdigit():
            print("Please enter a number from 1 to 9.")
            continue
        action = int(text) - 1
        if action not in legal:
            print("That square is taken or out of range. Try again.")
            continue
        return action


def random_policy(game):
    """Pick a uniformly random legal move."""
    return random.choice(game.legal_actions())


def play_game(policy_x, policy_o, verbose=True):
    """
    Play one game between two policies.

    Returns the winner (PLAYER_X, PLAYER_O, or EMPTY for a draw),
    or None if a policy quit mid-game.
    """
    policies = {PLAYER_X: policy_x, PLAYER_O: policy_o}
    game = TicTacToe()
    game.reset()

    while True:
        if verbose:
            show_board(game)

        action = policies[game.current_player](game)
        if action is None:
            if verbose:
                print("Game abandoned.")
            return None

        _, _, done = game.step(action)
        if done:
            winner = game.winner()
            if verbose:
                show_board(game)
                if winner == EMPTY:
                    print("It's a draw!")
                else:
                    print(f"Player {NAMES[winner]} wins!")
            return winner
