from argparse import Namespace

import runner
from games.tictactoe.rules import EMPTY, PLAYER_O, PLAYER_X


def test_parse_args_defaults(monkeypatch):
    monkeypatch.setattr("sys.argv", ["runner.py"])

    args = runner.parse_args()

    assert args.x == "human"
    assert args.o == "human"
    assert args.games == 1
    assert args.quiet is False


def test_parse_args_custom_arguments(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        [
            "runner.py",
            "--x",
            "random",
            "--o",
            "random",
            "--games",
            "1000",
            "--quiet",
        ],
    )

    args = runner.parse_args()

    assert args.x == "random"
    assert args.o == "random"
    assert args.games == 1000
    assert args.quiet is True


def test_print_summary(capsys):
    results = {
        PLAYER_X: 5,
        PLAYER_O: 3,
        EMPTY: 2,
    }

    runner.print_summary(results)

    captured = capsys.readouterr()

    assert captured.out == (
        "\nResults over 10 game(s):\n  X wins: 5\n  O wins: 3\n  Draws:  2\n"
    )


def test_main_plays_requested_number_of_games(monkeypatch):
    monkeypatch.setattr(
        runner,
        "parse_args",
        lambda: type(
            "Args",
            (),
            {
                "x": "random",
                "o": "random",
                "games": 3,
                "quiet": True,
            },
        )(),
    )

    winners = []

    def fake_play_game(policy_x, policy_o, verbose):
        winners.append((policy_x, policy_o, verbose))
        return PLAYER_X

    monkeypatch.setattr(runner, "play_game", fake_play_game)

    runner.main()

    assert len(winners) == 3
    assert all(verbose is False for _, _, verbose in winners)
    assert all(
        policy_x is runner.random_policy and policy_o is runner.random_policy
        for policy_x, policy_o, _ in winners
    )


def test_main_counts_wins_and_draws(monkeypatch, capsys):
    monkeypatch.setattr(
        runner,
        "parse_args",
        lambda: type(
            "Args",
            (),
            {
                "x": "random",
                "o": "random",
                "games": 3,
                "quiet": True,
            },
        )(),
    )

    winners = iter([PLAYER_X, PLAYER_O, EMPTY])

    monkeypatch.setattr(
        runner,
        "play_game",
        lambda policy_x, policy_o, verbose: next(winners),
    )

    runner.main()

    captured = capsys.readouterr()

    assert "Results over 3 game(s):" in captured.out
    assert "X wins: 1" in captured.out
    assert "O wins: 1" in captured.out
    assert "Draws:  1" in captured.out


def test_main_does_not_print_board_in_quiet_mode(monkeypatch, capsys):
    monkeypatch.setattr(
        runner,
        "parse_args",
        lambda: type(
            "Args",
            (),
            {
                "x": "random",
                "o": "random",
                "games": 1,
                "quiet": True,
            },
        )(),
    )

    calls = []

    def fake_play_game(policy_x, policy_o, verbose):
        calls.append(verbose)
        return PLAYER_X

    monkeypatch.setattr(runner, "play_game", fake_play_game)

    runner.main()

    captured = capsys.readouterr()

    assert calls == [False]
    assert "X: random | O: random" not in captured.out


def test_main_passes_verbose_when_not_quiet(monkeypatch, capsys):
    monkeypatch.setattr(
        runner,
        "parse_args",
        lambda: type(
            "Args",
            (),
            {
                "x": "random",
                "o": "random",
                "games": 1,
                "quiet": False,
            },
        )(),
    )

    calls = []

    def fake_play_game(policy_x, policy_o, verbose):
        calls.append(verbose)
        return PLAYER_X

    monkeypatch.setattr(runner, "play_game", fake_play_game)

    runner.main()

    captured = capsys.readouterr()

    assert calls == [True]
    assert "X: random | O: random. Squares are numbered 1-9." in captured.out


def test_main_stops_when_human_quits(monkeypatch):
    monkeypatch.setattr(
        runner,
        "parse_args",
        lambda: type(
            "Args",
            (),
            {
                "x": "human",
                "o": "random",
                "games": 10,
                "quiet": True,
            },
        )(),
    )

    calls = []

    def fake_play_game(policy_x, policy_o, verbose):
        calls.append(1)
        return None

    monkeypatch.setattr(runner, "play_game", fake_play_game)

    runner.main()

    assert len(calls) == 1


def test_main_asks_to_play_again_after_human_game(monkeypatch):
    monkeypatch.setattr(
        runner,
        "parse_args",
        lambda: Namespace(
            x="human",
            o="random",
            games=1,
            quiet=True,
        ),
    )

    results = iter([PLAYER_X, PLAYER_O])
    inputs = iter(["y", "n"])
    calls = []

    def fake_play_game(policy_x, policy_o, verbose):
        calls.append(1)
        return next(results)

    monkeypatch.setattr(runner, "play_game", fake_play_game)
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    runner.main()

    assert len(calls) == 2


def test_main_stops_when_user_declines_to_play_again(monkeypatch):
    monkeypatch.setattr(
        runner,
        "parse_args",
        lambda: type(
            "Args",
            (),
            {
                "x": "human",
                "o": "random",
                "games": 1,
                "quiet": True,
            },
        )(),
    )

    calls = []

    def fake_play_game(policy_x, policy_o, verbose):
        calls.append(1)
        return PLAYER_X

    monkeypatch.setattr(runner, "play_game", fake_play_game)
    monkeypatch.setattr("builtins.input", lambda _: "n")

    runner.main()

    assert len(calls) == 1
