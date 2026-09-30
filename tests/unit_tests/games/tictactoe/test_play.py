import pytest

from games.tictactoe.play import human_policy, play_game, random_policy, show_board
from games.tictactoe.rules import EMPTY, PLAYER_O, PLAYER_X, TicTacToe


def test_show_board(capsys):
    game = TicTacToe()
    game.board = [
        PLAYER_X,
        PLAYER_O,
        EMPTY,
        EMPTY,
        PLAYER_X,
        PLAYER_O,
        PLAYER_O,
        EMPTY,
        PLAYER_X,
    ]

    show_board(game)

    captured = capsys.readouterr()

    assert captured.out == (
        "\n X | O | 3\n---+---+---\n 4 | X | O\n---+---+---\n O | 8 | X\n\n"
    )


def test_human_policy_accepts_valid_move(monkeypatch):
    game = TicTacToe()

    monkeypatch.setattr("builtins.input", lambda _: "5")

    action = human_policy(game)

    assert action == 4


def test_human_policy_converts_input_to_zero_based_index(monkeypatch):
    game = TicTacToe()

    monkeypatch.setattr("builtins.input", lambda _: "1")

    action = human_policy(game)

    assert action == 0


def test_human_policy_accepts_uppercase_quit(monkeypatch):
    game = TicTacToe()

    monkeypatch.setattr("builtins.input", lambda _: "Q")

    action = human_policy(game)

    assert action is None


def test_human_policy_accepts_quit_word(monkeypatch):
    game = TicTacToe()

    monkeypatch.setattr("builtins.input", lambda _: "quit")

    action = human_policy(game)

    assert action is None


def test_human_policy_rejects_non_numeric_input(monkeypatch, capsys):
    game = TicTacToe()
    inputs = iter(["abc", "5"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    action = human_policy(game)

    captured = capsys.readouterr()

    assert action == 4
    assert "Please enter a number from 1 to 9." in captured.out


def test_human_policy_rejects_illegal_move(monkeypatch, capsys):
    game = TicTacToe()
    game.board[4] = PLAYER_X

    inputs = iter(["5", "6"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    action = human_policy(game)

    captured = capsys.readouterr()

    assert action == 5
    assert "That square is taken or out of range. Try again." in captured.out


@pytest.mark.parametrize("input_text", ["0", "10"])
def test_human_policy_rejects_out_of_range_move(monkeypatch, capsys, input_text):
    game = TicTacToe()
    inputs = iter([input_text, "1"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    action = human_policy(game)

    captured = capsys.readouterr()

    assert action == 0
    assert "That square is taken or out of range. Try again." in captured.out


def test_human_policy_rejects_negative_number(monkeypatch, capsys):
    game = TicTacToe()
    inputs = iter(["-1", "1"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    action = human_policy(game)

    captured = capsys.readouterr()

    assert action == 0
    assert "Please enter a number from 1 to 9." in captured.out


def test_random_policy_chooses_from_legal_actions(monkeypatch):
    game = TicTacToe()
    game.board[0] = PLAYER_X
    game.board[4] = PLAYER_O

    selected = []

    def fake_choice(actions):
        selected.append(actions)
        return actions[0]

    monkeypatch.setattr("games.tictactoe.play.random.choice", fake_choice)

    action = random_policy(game)

    assert selected == [[1, 2, 3, 5, 6, 7, 8]]
    assert action == 1


def test_play_game_returns_x_winner():
    moves = iter([0, 3, 1, 4, 2])

    def policy(game):
        return next(moves)

    winner = play_game(policy, policy, verbose=False)

    assert winner == PLAYER_X


def test_play_game_returns_o_winner():
    x_moves = iter([0, 2, 3])
    o_moves = iter([1, 4, 7])

    def policy_x(game):
        return next(x_moves)

    def policy_o(game):
        return next(o_moves)

    winner = play_game(policy_x, policy_o, verbose=False)

    assert winner == PLAYER_O


def test_play_game_returns_draw():
    moves = iter([0, 1, 2, 4, 3, 5, 7, 6, 8])

    def policy(game):
        return next(moves)

    winner = play_game(policy, policy, verbose=False)

    assert winner == EMPTY


def test_play_game_returns_none_when_x_quits():
    def quit_policy(game):
        return None

    winner = play_game(quit_policy, quit_policy, verbose=False)

    assert winner is None


def test_play_game_returns_none_when_o_quits():
    moves = iter([0])

    def policy_x(game):
        return next(moves)

    def policy_o(game):
        return None

    winner = play_game(policy_x, policy_o, verbose=False)

    assert winner is None


def test_play_game_verbose_false_prints_nothing(capsys):
    moves = iter([0, 3, 1, 4, 2])

    def policy(game):
        return next(moves)

    play_game(policy, policy, verbose=False)

    captured = capsys.readouterr()

    assert captured.out == ""


def test_play_game_verbose_true_prints_game_result(capsys):
    moves = iter([0, 3, 1, 4, 2])

    def policy(game):
        return next(moves)

    winner = play_game(policy, policy, verbose=True)

    captured = capsys.readouterr()

    assert winner == PLAYER_X
    assert "Player X wins!" in captured.out


def test_play_game_verbose_true_prints_draw(capsys):
    moves = iter([0, 1, 2, 4, 3, 5, 7, 6, 8])

    def policy(game):
        return next(moves)

    winner = play_game(policy, policy, verbose=True)

    captured = capsys.readouterr()

    assert winner == EMPTY
    assert "It's a draw!" in captured.out


def test_play_game_verbose_true_prints_abandoned(capsys):
    def quit_policy(game):
        return None

    winner = play_game(quit_policy, quit_policy, verbose=True)

    captured = capsys.readouterr()

    assert winner is None
    assert "Game abandoned." in captured.out
