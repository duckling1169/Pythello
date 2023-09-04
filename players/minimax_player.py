from game.enums import Color
from game.board import Board
from game.point import Point
from players.player import Player
import random
import copy

class MiniMaxPlayer(Player):

    def __init__(self, color: Color, max_depth:int = 1):
        self.max_depth = max_depth        
        super().__init__(color)

    def play(self, board: Board) -> Point:
        return self.minimax_with_heuristics(board, self.color, self.max_depth)[0]

    def minimax_with_heuristics(self, board: Board, color: Color, depth: int) -> (Point, int):
        """
        Perform MiniMax search with heuristics to find the best move.

        Args:
            board (Board): The current game board.
            color (Color): The color of the player for whom to find the best move.
            depth (int): The maximum search depth.

        Returns:
            Tuple[Point, int]: The best move and its associated score.
        """
        # If the depth limit is reached, return None and a score of 0.
        if depth == 0:
            return None, 0 

        best_move, best_score = None, float('-inf')

        # Calculate existing heuristic values for the current player
        existing_board_square_heuristic = board.square_heuristic(color)
        existing_board_stability_heuristic = board.stability_heuristic(color)

        for move in board.get_legal_moves(color):
            board_copy = copy.deepcopy(board)
            board_copy.place_and_flip_discs(move, color)

            # Determine the opposite player's color
            opposite_color = Color.WHITE if color == Color.BLACK else Color.BLACK

            # Recursively find the best move for the opposite player
            _, opposite_score = self.minimax_with_heuristics(board_copy, opposite_color, depth - 1)

            # Calculate new heuristic values after the move
            new_square, new_stability = board_copy.square_heuristic(color), board_copy.stability_heuristic(color)

            # Calculate the score based on heuristics and the opposite player's score
            score = new_square - existing_board_square_heuristic + new_stability - existing_board_stability_heuristic + opposite_score

            print(color, move, score, new_square-existing_board_square_heuristic, new_stability-existing_board_stability_heuristic, opposite_score)

            if score == best_score:
                # Introduce randomness for equally scored moves
                best_move = random.choice([best_move, move])
            elif score > best_score:
                # Update the best move if a better one is found
                best_score, best_move = score, move

        # Adjust the score based on the current player's color
        best_score *= 1 if color == self.color else -1
        return best_move, best_score
