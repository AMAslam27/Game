from pathlib import PurePath


class FakeGame:
    def __init__(self, board, current_player):
        self.board = board.copy()
        self.current_player = current_player

    def legal_actions(self):
        return [i for i, cell in enumerate(self.board) if cell == 0]

    def is_terminal(self):
        lines = (
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6),
        )
        return not self.legal_actions() or any(
            self.board[a] != 0 and self.board[a] == self.board[b] == self.board[c]
            for a, b, c in lines
        )


class FakeAxes:
    def __init__(self):
        self.bar_calls = []
        self.bar_label_calls = []

    def bar(self, labels, values, **kwargs):
        self.bar_calls.append((labels, values, kwargs))
        return "bars"

    def set_ylim(self, *args):
        pass

    def set_ylabel(self, label):
        pass

    def set_title(self, title):
        self.title = title

    def bar_label(self, bars, **kwargs):
        self.bar_label_calls.append((bars, kwargs))


class FakeFigure:
    def __init__(self, **kwargs):
        self.axes = FakeAxes()
        self.saved = []
        self.cleared = False
        self.save_error = None

    def subplots(self):
        return self.axes

    def tight_layout(self):
        pass

    def savefig(self, path, **kwargs):
        self.saved.append((path, kwargs))
        if self.save_error:
            raise self.save_error

    def clear(self):
        self.cleared = True


class FakePath:
    def __init__(self, path):
        self.path = PurePath(path)
        self.mkdir_calls = []

    @property
    def parent(self):
        return self

    def mkdir(self, **kwargs):
        self.mkdir_calls.append(kwargs)


class FakePlotter:
    def __init__(self, result=None):
        self.calls = []
        self.result = result

    def __call__(self, results, policy_x, policy_o, **kwargs):
        self.calls.append((results.copy(), policy_x, policy_o, kwargs))
        return self.result


class FakeCursor:
    def __init__(self, lastrowid):
        self.lastrowid = lastrowid


class FakeConnection:
    def __init__(self):
        self.executions = []
        self.scripts = []
        self.commits = 0
        self.rollbacks = 0
        self.closed = False
        self.next_id = 1
        self.error = None

    def execute(self, sql, parameters=()):
        self.executions.append((" ".join(sql.split()), parameters))
        if self.error is not None:
            raise self.error
        run_id = self.next_id
        if "INSERT INTO runs" in sql:
            self.next_id += 1
        return FakeCursor(run_id)

    def executescript(self, sql):
        self.scripts.append(sql)
        if self.error is not None:
            raise self.error

    def __enter__(self):
        return self

    def __exit__(self, error_type, error, traceback):
        if error_type is None:
            self.commits += 1
        else:
            self.rollbacks += 1
        return False

    def close(self):
        self.closed = True
