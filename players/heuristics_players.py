from game.enums import Color
from game.board import Board
from game.point import Point
from players.player import Player
import copy

class HeuristicPlayer(Player):

    def __init__(self, color: Color, heuristic_name:str = "square_heuristic"):
        """
        Initialize a HeuristicPlayer instance.

        Args:
            color (Color): The player's color.
            heuristic_func (Callable[[Board, Color], int]): The heuristic function to use.
        """
        self.heuristic = getattr(Board, heuristic_name) if hasattr(Board, heuristic_name) else None
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
            heuristic_value = self.heuristic(board_copy, self.color)

            if current_best < heuristic_value:
                current_best = heuristic_value
                best_move = move

        return best_move