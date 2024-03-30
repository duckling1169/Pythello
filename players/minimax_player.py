from game.enums import Color
from game.board import Board
from game.point import Point
from players.player import Player

import random
import copy
from typing import List

class MiniMaxPlayer(Player):

    def __init__(self, color: Color, heuristic_names: List[str] = ['square_heuristic', 'mobility_heuristic'], max_depth:int = 2):
        """
        A player class implementing the MiniMax algorithm with heuristic evaluation.

        Attributes:
            color (Color): The color of the player.
            heuristic_names (List[str]): The names of the heuristic functions to use.
            max_depth (int): The maximum depth to search in the MiniMax algorithm.
            heuristics (function): The heuristic functions to evaluate board states.
        """
        self.heuristics = [ getattr(Board, name) if hasattr(Board, name) else None for name in heuristic_names ]
        self.max_depth = max_depth
        super().__init__(color)

    def play(self, board: Board) -> Point:
        """
        Chooses the best move for the player using MiniMax with heuristics.

        Args:
            board (Board): The current game board state.

        Returns:
            Point: The best move to play based on MiniMax and heuristics.
        """
        move, score = self.minimax_with_heuristics(board, self.color, self.max_depth, self.heuristics)
        return move

    def minimax_with_heuristics(self, board: Board, color: Color, depth: int, heuristics) -> tuple[Point, int]:
        """
        Perform MiniMax search with given heuristic to find the best move.

        Args:
            board (Board): The current game board.
            color (Color): The color of the player for whom to find the best move.
            depth (int): The maximum search depth.
            heuristics: The heuristic function to min-max.

        Returns:
            Tuple[Point, int]: The best move and its associated score.
        """ 
        # If the game is over, return None and the current color's score.
        if depth == 0:
            heuristic_value = sum(heuristic(board, color) for heuristic in heuristics)
            return None, heuristic_value
        
        if board.is_game_over():
            return None, board.winner_heuristic(color)

        best_move, best_score = None, float('-inf')

        for move in board.get_legal_moves(color):
            board_copy = copy.deepcopy(board)
            board_copy.place_and_flip_discs(move, color)

            # Determine the opposite player's color
            opposite_color = Color.WHITE if color == Color.BLACK else Color.BLACK

            # Recursively find the best move for the opposite player
            _, opposite_score = self.minimax_with_heuristics(board_copy, opposite_color, depth - 1, heuristics)

            # Calculate new heuristic values after the move
            heuristic_values = {str(heuristic.__name__): heuristic(board_copy, self.color) for heuristic in self.heuristics}
            player_score = sum(heuristic(board_copy, color) for heuristic in heuristics)

            # Calculate the score based on heuristics and the opposite player's score
            if opposite_score < 0:
                if player_score < 0: # -2, -4 = 2 | -10, -5 = -5 | -1, -1 = 0
                    score = abs(opposite_score) - abs(player_score) # 4-2 | 5-10, 1-1
                else: # 10, -5 = 15 | 0, -5 = 5
                    score = player_score - opposite_score
            else: # 20, 10 = 10 | 10, 25 = -15
                score = player_score - opposite_score
            
            print(move, heuristic_values, player_score, opposite_score, score)
            score = player_score
            
            # print(f"Board after move: {board_copy}Depth: {depth}, Move: {move}, Current Player: {color}, Player Score: {player_score}, Opponent Score: {opposite_score}, Combined Score: {score}")
            if score == best_score: # Introduce randomness for equally scored moves
                best_move = random.choice([best_move, move])
            elif score > best_score: # Update the best move if a better one is found
                best_score, best_move = score, move

        return best_move, best_score
