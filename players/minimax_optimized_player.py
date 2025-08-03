from game.enums import Color
from game.board import Board
from game.point import Point
from players.player import Player

import random
from typing import List


class OptimizedMiniMaxPlayer(Player):
    """
    An optimized minimax player that uses move/undo instead of deep copying
    for significantly better performance.
    """

    def __init__(self, color: Color, heuristic_names: List[str] = ['square_heuristic', 'mobility_heuristic'], max_depth: int = 4):
        """
        Initialize an optimized MiniMax player.

        Args:
            color (Color): The color of the player.
            heuristic_names (List[str]): The names of the heuristic functions to use.
            max_depth (int): The maximum depth to search in the MiniMax algorithm.
        """
        self.heuristic_names = heuristic_names
        self.heuristics: List[function] = [getattr(Board, name) if hasattr(Board, name) else None for name in heuristic_names]
        self.max_depth = max_depth
        super().__init__(color)

    def play(self, board: Board) -> Point:
        """
        Choose the best move using optimized MiniMax with alpha-beta pruning.

        Args:
            board (Board): The current game board state.

        Returns:
            Point: The best move to play.
        """
        move, score = self.minimax_optimized(board, self.color, self.max_depth, 
                                           float('-inf'), float('inf'), True)
        return move

    def minimax_optimized(self, board: Board, color: Color, depth: int, 
                         alpha: float, beta: float, maximizing_player: bool = True) -> tuple[Point, float]:
        """
        Optimized MiniMax search using move/undo instead of deep copying.

        Args:
            board (Board): The current game board.
            color (Color): The color of the current player.
            depth (int): The remaining search depth.
            alpha (float): Alpha value for alpha-beta pruning.
            beta (float): Beta value for alpha-beta pruning.
            maximizing_player (bool): Whether this is the maximizing player's turn.

        Returns:
            Tuple[Point, float]: The best move and its score.
        """
        if depth == 0 or board.is_game_over():
            if board.is_game_over():
                return None, board.winner_heuristic(self.color)
            else:
                heuristic_value = sum(heuristic(board, self.color) for heuristic in self.heuristics)
                return None, heuristic_value

        legal_moves = board.get_ordered_legal_moves(color)
        
        # If no legal moves, skip to opponent
        if not legal_moves:
            opposite_color = Color.WHITE if color == Color.BLACK else Color.BLACK
            _, score = self.minimax_optimized(board, opposite_color, depth - 1, alpha, beta, not maximizing_player)
            return None, score

        best_move = None
        
        if maximizing_player:
            max_eval = float('-inf')
            
            for move in legal_moves:
                # Make move
                flipped_discs = board.make_move(move, color)
                
                # Recursive call
                opposite_color = Color.WHITE if color == Color.BLACK else Color.BLACK
                _, eval_score = self.minimax_optimized(board, opposite_color, depth - 1, alpha, beta, False)
                
                # Undo move
                board.undo_move(move, color, flipped_discs)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                elif eval_score == max_eval and random.random() < 0.5:
                    best_move = move
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Alpha-beta pruning
                    
            return best_move, max_eval
        else:
            min_eval = float('inf')
            
            for move in legal_moves:
                # Make move
                flipped_discs = board.make_move(move, color)
                
                # Recursive call
                opposite_color = Color.WHITE if color == Color.BLACK else Color.BLACK
                _, eval_score = self.minimax_optimized(board, opposite_color, depth - 1, alpha, beta, True)
                
                # Undo move
                board.undo_move(move, color, flipped_discs)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                elif eval_score == min_eval and random.random() < 0.5:
                    best_move = move
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha-beta pruning
                    
            return best_move, min_eval