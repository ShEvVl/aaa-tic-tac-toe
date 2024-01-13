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
        # Проверка строк, столбцов и диагоналей
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or all(
                self.board[j][i] == player for j in range(3)
            ):
                return True
        if (
            self.board[0][0] == self.board[1][1] == self.board[2][2] == player
            or self.board[0][2]
            == self.board[1][1]
            == self.board[2][0]
            == player
        ):
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
