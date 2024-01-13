import pytest
from src.ttt_game import TicTacToeGame


@pytest.fixture
def ttt_game():
    return TicTacToeGame()


def test_initialization(ttt_game):
    assert ttt_game.board == [
        ["." for _ in range(3)] for _ in range(3)
    ], "Игровое поле должно быть пустым при инициализации"


def test_player_move(ttt_game):
    assert (
        ttt_game.make_move(0, 0, TicTacToeGame.CROSS) is True
    ), "Ход должен быть возможен"
    assert (
        ttt_game.board[0][0] == TicTacToeGame.CROSS
    ), "Игровое поле должно обновляться после хода"


def test_win_condition(ttt_game):
    ttt_game.board = [
        [
            TicTacToeGame.CROSS,
            TicTacToeGame.FREE_SPACE,
            TicTacToeGame.FREE_SPACE,
        ],
        [
            TicTacToeGame.CROSS,
            TicTacToeGame.FREE_SPACE,
            TicTacToeGame.FREE_SPACE,
        ],
        [
            TicTacToeGame.CROSS,
            TicTacToeGame.FREE_SPACE,
            TicTacToeGame.FREE_SPACE,
        ],
    ]
    assert (
        ttt_game.check_win(TicTacToeGame.CROSS) is True
    ), "Должна быть определена победа"


def test_draw_condition(ttt_game):
    ttt_game.board = [
        [TicTacToeGame.CROSS, TicTacToeGame.ZERO, TicTacToeGame.CROSS],
        [TicTacToeGame.CROSS, TicTacToeGame.CROSS, TicTacToeGame.ZERO],
        [TicTacToeGame.ZERO, TicTacToeGame.CROSS, TicTacToeGame.ZERO],
    ]
    assert ttt_game.is_draw() is True, "Должна быть определена ничья"


def test_reset_game(ttt_game):
    ttt_game.board = [
        [TicTacToeGame.CROSS, TicTacToeGame.ZERO, TicTacToeGame.CROSS],
        [TicTacToeGame.CROSS, TicTacToeGame.CROSS, TicTacToeGame.ZERO],
        [TicTacToeGame.ZERO, TicTacToeGame.CROSS, TicTacToeGame.ZERO],
    ]
    ttt_game.reset()
    assert ttt_game.board == [
        ["." for _ in range(3)] for _ in range(3)
    ], "Игра должна сбрасываться в начальное состояние"
