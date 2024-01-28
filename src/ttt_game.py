from typing import List, Tuple


class TicTacToeGame:
    """
    Класс для логики игры в крестики-нолики.
    """

    FREE_SPACE = "."
    CROSS = "X"
    ZERO = "O"

    def __init__(self) -> None:
        """
        Инициализация новой игры.
        """
        self.board: List[List[str]] = [
            [self.FREE_SPACE for _ in range(3)] for _ in range(3)
        ]

    def make_move(self, row: int, col: int, player: str) -> bool:
        """
        Сделать ход в игре.

        :param row: Ряд для хода.
        :param col: Колонка для хода.
        :param player: Игрок, делающий ход ('X' или 'O').
        :return: True, если ход успешен, иначе False.
        """
        if self.board[row][col] == self.FREE_SPACE:
            self.board[row][col] = player
            return True
        return False

    def check_win(self, player: str) -> bool:
        """
        Проверить, выиграл ли игрок.

        :param player: Игрок для проверки ('X' или 'O').
        :return: True, если игрок выиграл, иначе False.
        """
        win_conditions = [
            ['00', '01', '02'],
            ['10', '11', '12'],
            ['20', '21', '22'],
            ['00', '10', '20'],
            ['01', '11', '21'],
            ['02', '12', '22'],
            ['00', '11', '22'],
            ['02', '11', '20'],
        ]

        for condition in win_conditions:
            if all(self.board[int(pos[0])][int(pos[1])] == player for pos in condition):
                return True
        return False

    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """
        Получить список пустых клеток на доске.

        :return: Список кортежей координат пустых клеток.
        """
        return [
            (i, j)
            for i in range(3)
            for j in range(3)
            if self.board[i][j] == self.FREE_SPACE
        ]

    def is_draw(self) -> bool:
        """
        Проверить, является ли текущее состояние игры ничьей.

        :return: True, если ничья, иначе False.
        """
        return all(
            self.board[i][j] != self.FREE_SPACE
            for i in range(3)
            for j in range(3)
        )

    def reset(self) -> None:
        """
        Сбросить игровое поле в начальное состояние.
        """
        self.board = [[self.FREE_SPACE for _ in range(3)] for _ in range(3)]
