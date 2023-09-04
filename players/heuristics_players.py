from game.enums import Color
from game.board import Board
from game.point import Point
from players.player import Player
import copy
from typing import Callable

class HeuristicPlayer(Player):
    def __init__(self, color: Color, heuristic_func: Callable[[Board, Color], int]):
        """
        Initialize a HeuristicPlayer instance.

        Args:
            color (Color): The player's color.
            heuristic_func (Callable[[Board, Color], int]): The heuristic function to use.
        """
        super().__init__(color)
        self.heuristic_func = heuristic_func

    def play(self, board: Board) -> Point:
        """
        Choose the best legal move based on the specified heuristic function.

        Args:
            board (Board): The current game board.

        Returns:
            Point: The best move according to the specified heuristic.
        """
        legal_moves = board.get_legal_moves(self.color)

        current_best = float('-inf')
        best_move = None
        for move in legal_moves:
            board_copy = copy.deepcopy(board)
            board_copy.place_and_flip_discs(move, self.color)
            heuristic_value = self.heuristic_func(board_copy, self.color)

            if current_best < heuristic_value:
                current_best = heuristic_value
                best_move = move

        return best_move

def square_heuristic(board: Board, color: Color) -> int:
    """
    Calculate the square heuristic for the specified color.

    Args:
        board (Board): The game board.
        color (Color): The color for which the heuristic is calculated.

    Returns:
        int: The square heuristic value.
    """
    return board.square_heuristic(color)

def stability_heuristic(board: Board, color: Color) -> int:
    """
    Calculate the stability heuristic for the specified color.

    Args:
        board (Board): The game board.
        color (Color): The color for which the heuristic is calculated.

    Returns:
        int: The stability heuristic value.
    """
    return board.stability_heuristic(color)

def mobility_heuristic(board: Board, color: Color) -> int:
    """
    Calculate the mobility heuristic for the specified color.

    Args:
        board (Board): The game board.
        color (Color): The color for which the heuristic is calculated.

    Returns:
        int: The mobility heuristic value.
    """
    return board.mobility_heuristic(color)
