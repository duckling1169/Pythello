from players.player import Player
from game.enums import DiscEnum
from game.board import Board
from game.point import Point
import copy

class MiniMaxPlayer(Player):

    def __init__(self, color:DiscEnum):
        super().__init__(color)

    def play(self, board: Board) -> Point:
        best_move, _ = self.minimax(board, True, self.color)
        return best_move

    def minimax(self, board: Board, maximizing_player: bool, color: DiscEnum, depth: int = 7, alpha: float = float('-inf'), beta: float = float('inf')):
        if depth == 0 or board.is_game_over() or not board.get_all_playable_points(self.color):
            return None, board.calculate_color_points(color)

        best_move = None

        if maximizing_player:
            max_eval = float('-inf')  # Initialize the max_eval to negative infinity
            for move in board.get_all_playable_points(color):
                copy_board = copy.deepcopy(board)
                copy_board.can_place_disc_and_flip(move, color)  # Apply the move to the copy
                _, eval = self.minimax(copy_board, False, color, depth - 1, alpha, beta)  # Recursive call for opponent's turn
                if eval > max_eval:  # If the evaluation is better than the current max
                    max_eval = eval  # Update max_eval with the new evaluation
                    best_move = move  # Update the best move
                alpha = max(alpha, eval)  # Update alpha with the new max
                if beta <= alpha:
                    break  # Beta cutoff: prune this branch if it's worse than the current best
            return best_move, max_eval

        else:  # If it's the minimizing player's turn
            min_eval = float('inf')  # Initialize the min_eval to positive infinity
            opponent_color = DiscEnum.BLACK if color == DiscEnum.WHITE else DiscEnum.WHITE  # Determine the opponent's color
            for move in board.get_all_playable_points(opponent_color):
                copy_board = copy.deepcopy(board)
                copy_board.can_place_disc_and_flip(move, opponent_color)  # Apply the move to the copy
                _, eval = self.minimax(copy_board, True, color, depth - 1, alpha, beta)  # Recursive call for player's turn
                if eval < min_eval:  # If the evaluation is better than the current min
                    min_eval = eval  # Update min_eval with the new evaluation
                    best_move = move  # Update the best move
                beta = min(beta, eval)  # Update beta with the new min
                if beta <= alpha:
                    break  # Alpha cutoff: prune this branch if it's worse than the current best
            return best_move, min_eval