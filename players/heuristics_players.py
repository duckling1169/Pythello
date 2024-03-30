from game.enums import Color
from game.board import Board
from game.point import Point
from players.player import Player

import copy
from typing import List

class HeuristicPlayer(Player):

    def __init__(self, color: Color, heuristic_names: List[str] = ['square_heuristic', 'mobility_heuristic']):
        """
        Initialize a HeuristicPlayer instance.

        Args:
            color (Color): The player's color.
            heuristic_names (List[str]): The heuristic function to use.
        """
        self.heuristics = [ getattr(Board, name) if hasattr(Board, name) else None for name in heuristic_names ]
        super().__init__(color)

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
            # heuristic_values = {str(heuristic.__name__): heuristic(board_copy, self.color) for heuristic in self.heuristics}
            heuristic_value = sum(heuristic(board_copy, self.color) for heuristic in self.heuristics)
            if current_best < heuristic_value:
                current_best = heuristic_value
                best_move = move

        return best_move