from game.enums import Color
from game.board import Board
from game.point import Point
from players.player import Player
import random
import copy

class MiniMaxPlayer(Player):

    def __init__(self, color: Color, max_depth:int = 1, heuristic_name:str = "square_heuristic"):
        """
        A player class implementing the MiniMax algorithm with heuristic evaluation.

        Attributes:
            color (Color): The color of the player.
            max_depth (int): The maximum depth to search in the MiniMax algorithm.
            heuristic_name (str): The name of the heuristic function to use.
            heuristic (function): The heuristic function to evaluate board states.
        """
        self.max_depth = max_depth
        self.heuristic = getattr(Board, heuristic_name) if hasattr(Board, heuristic_name) else None
        super().__init__(color)

    def play(self, board: Board) -> Point:
        return self.minimax_with_heuristics(board, self.color, self.max_depth, self.heuristic)[0]

    def minimax_with_heuristics(self, board: Board, color: Color, depth: int, heuristic) -> (Point, int):
        """
        Perform MiniMax search with given heuristic to find the best move.

        Args:
            board (Board): The current game board.
            color (Color): The color of the player for whom to find the best move.
            depth (int): The maximum search depth.
            heuristic: The heuristic function to min-max.

        Returns:
            Tuple[Point, int]: The best move and its associated score.
        """ 
        # If the game is over, return None and the current color's score.
        if depth == 0 or board.is_game_over():
            return None, board.get_points_for_color(color)

        best_move, best_score = None, float('-inf')

        # Calculate existing heuristic values for the current player
        prev_heuristic = heuristic(board, color)

        for move in board.get_legal_moves(color):
            board_copy = copy.deepcopy(board)
            board_copy.place_and_flip_discs(move, color)

            # Determine the opposite player's color
            opposite_color = Color.WHITE if color == Color.BLACK else Color.BLACK

            # Recursively find the best move for the opposite player
            _, opposite_score = self.minimax_with_heuristics(board_copy, opposite_color, depth - 1, heuristic)

            # Calculate new heuristic values after the move
            new_heuristic = heuristic(board_copy, color)

            # Calculate the score based on heuristics and the opposite player's score
            score = new_heuristic - prev_heuristic + opposite_score

            if score == best_score:
                # Introduce randomness for equally scored moves
                best_move = random.choice([best_move, move])
            elif score > best_score:
                # Update the best move if a better one is found
                best_score, best_move = score, move

        # Adjust the score based on the current player's color
        best_score *= 1 if color == self.color else -1
        return best_move, best_score
