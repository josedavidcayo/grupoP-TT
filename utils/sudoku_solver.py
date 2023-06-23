# imports
import random
from copy import *


class SudokuBoard:
    def __init__(self, board: list[list] = None):
        if board is None:
            board = []

        self.board = board
        self.board_size = len(self.board)
        self.valid_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.difficulty = {
            'Principiante': 24,
            'Facil': 37,
            'Medio': 47,
            'Dificil': random.randint(49, 53),
            'Extremo': random.randint(54, 59),
        }

    def generate(self):
        """Generar un tablero de sudoku resuelto"""
        self.set_empty_board()
        randomize_first_row = self.valid_numbers.copy()
        random.shuffle(randomize_first_row)  # aleatorizar una lista 1-9
        self.board[0] = randomize_first_row  # setear la primera fila como lista aleatoria
        self.board_length()
        self.solve()
        return self.board

    def scrambled_board(self, difficulty_setting: str = 'Principiante') -> list[list]:
        """Una función para eliminar números del tablero de sudoku completamente resuelto según la dificultad

        :parametro difficulty_setting: Toma las entradas de dificultad `principiante` (predeterminado), `fácil`, `medio`, `difícil`, `extremo`
        :return: tablero de sudoku sin resolver
        """

        sudoku_copy = deepcopy(self.board)
        difficulty_setting = difficulty_setting.lower()
        removals = self.difficulty.get(difficulty_setting, 24)

        i = 0
        while i < removals:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if sudoku_copy[row][col] != 0:
                sudoku_copy[row][col] = 0
                i += 1

        return sudoku_copy

    def board_length(self):
        self.board_size = len(self.board)

    def set_empty_board(self):
        self.board = [[0] * 9 for _ in range(9)]

    def set_board(self, board):
        self.board = board
        print(*self.board, sep='\n')
        self.board_size = len(self.board) if self.board else 0

    def is_solvable(self):
        return bool(self.solve())

    def is_valid(self, row, col, num):
        """Validar que el número en el tablero sea válido tanto en la fila, la columna como en el cuadro de 3x3"""

        # Comprueba si el número ya está presente en la columna
        for i in range(9):
            if self.board[i][col] == num:
                return False

        # Compruebe si el número ya está presente en la cuadrícula de 3x3
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j] == num:
                    return False

        # Si el número es válido, devuelve True
        return num not in self.board[row]

    def solve(self):
        """Resolver el tablero de sudoku usando recursividad"""
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == 0:
                    for n in range(1, 10):
                        if self.is_valid(row, col, n):
                            self.board[row][col] = n
                            if self.solve():
                                return self.board
                            self.board[row][col] = 0
                    return False
        return True


