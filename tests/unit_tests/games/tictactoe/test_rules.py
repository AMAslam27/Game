import pytest

from games.tictactoe.rules import (
    EMPTY,
    PLAYER_O,
    PLAYER_X,
    TicTacToe,
)


def test_initial_state():
    game = TicTacToe()

    assert game.board == [EMPTY] * 9
    assert game.current_player == PLAYER_X


def test_reset_returns_empty_board_and_sets_player_x():
    game = TicTacToe()

    game.board[0] = PLAYER_X
    game.current_player = PLAYER_O

    board = game.reset()

    assert board == [EMPTY] * 9
    assert game.board == [EMPTY] * 9
    assert game.current_player == PLAYER_X


def test_reset_returns_copy_of_board():
    game = TicTacToe()

    board = game.reset()
    board[0] = PLAYER_X

    assert game.board == [EMPTY] * 9


def test_legal_actions_returns_all_empty_squares():
    game = TicTacToe()

    assert game.legal_actions() == list(range(9))


def test_legal_actions_excludes_occupied_squares():
    game = TicTacToe()

    game.board[0] = PLAYER_X
    game.board[4] = PLAYER_O

    assert game.legal_actions() == [1, 2, 3, 5, 6, 7, 8]


def test_step_places_player_on_board():
    game = TicTacToe()

    board, reward, done = game.step(4)

    assert board[4] == PLAYER_X
    assert game.board[4] == PLAYER_X
    assert reward == 0.0
    assert done is False


def test_step_returns_copy_of_board():
    game = TicTacToe()

    board, _, _ = game.step(0)
    board[1] = PLAYER_O

    assert game.board[1] == EMPTY


def test_step_switches_player_after_non_terminal_move():
    game = TicTacToe()

    game.step(0)

    assert game.current_player == PLAYER_O

    game.step(1)

    assert game.current_player == PLAYER_X


def test_step_rejects_occupied_square():
    game = TicTacToe()

    game.step(0)

    with pytest.raises(ValueError, match="Illegal action: 0"):
        game.step(0)


def test_step_rejects_invalid_action():
    game = TicTacToe()

    for action in (-1, 9, 10):
        with pytest.raises(ValueError, match=f"Illegal action: {action}"):
            game.step(action)


def test_x_wins_with_top_row():
    game = TicTacToe()

    game.step(0)  # X
    game.step(3)  # O
    game.step(1)  # X
    game.step(4)  # O
    board, reward, done = game.step(2)  # X

    assert board == [
        PLAYER_X,
        PLAYER_X,
        PLAYER_X,
        PLAYER_O,
        PLAYER_O,
        EMPTY,
        EMPTY,
        EMPTY,
        EMPTY,
    ]
    assert reward == 1.0
    assert done is True
    assert game.winner() == PLAYER_X


def test_o_wins_with_middle_column():
    game = TicTacToe()

    game.step(0)  # X
    game.step(1)  # O
    game.step(3)  # X
    game.step(4)  # O
    game.step(8)  # X
    board, reward, done = game.step(7)  # O

    assert board[1] == PLAYER_O
    assert board[4] == PLAYER_O
    assert board[7] == PLAYER_O
    assert reward == 1.0
    assert done is True
    assert game.winner() == PLAYER_O


def test_winner_detects_all_win_lines():
    winning_lines = (
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    )

    for line in winning_lines:
        game = TicTacToe()

        for index in line:
            game.board[index] = PLAYER_X

        assert game.winner() == PLAYER_X


def test_winner_returns_empty_when_there_is_no_winner():
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
        EMPTY,
    ]

    assert game.winner() == EMPTY


def test_winner_can_detect_o_win():
    game = TicTacToe()

    game.board[0] = PLAYER_O
    game.board[4] = PLAYER_O
    game.board[8] = PLAYER_O

    assert game.winner() == PLAYER_O


def test_step_detects_draw():
    game = TicTacToe()

    moves = (
        0,  # X
        1,  # O
        2,  # X
        4,  # O
        3,  # X
        5,  # O
        7,  # X
        6,  # O
        8,  # X
    )

    for action in moves[:-1]:
        _, reward, done = game.step(action)
        assert reward == 0.0
        assert done is False

    board, reward, done = game.step(moves[-1])

    assert board == [
        PLAYER_X,
        PLAYER_O,
        PLAYER_X,
        PLAYER_X,
        PLAYER_O,
        PLAYER_O,
        PLAYER_O,
        PLAYER_X,
        PLAYER_X,
    ]
    assert reward == 0.0
    assert done is True
    assert game.winner() == EMPTY
    assert game.legal_actions() == []


def test_is_terminal_is_false_for_new_game():
    game = TicTacToe()

    assert game.is_terminal() is False


def test_is_terminal_is_false_during_game():
    game = TicTacToe()

    game.step(0)

    assert game.is_terminal() is False


def test_is_terminal_is_true_after_x_wins():
    game = TicTacToe()

    game.step(0)
    game.step(3)
    game.step(1)
    game.step(4)
    game.step(2)

    assert game.is_terminal() is True


def test_is_terminal_is_true_after_draw():
    game = TicTacToe()

    moves = (0, 1, 2, 4, 3, 5, 7, 6, 8)

    for action in moves:
        game.step(action)

    assert game.is_terminal() is True


def test_render_prints_board(capsys):
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

    game.render()

    captured = capsys.readouterr()

    assert captured.out == ("X O .\n. X O\nO . X\n\n")
