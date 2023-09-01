from game.point import Point
from game.enums import DiscEnum
from game.board import Board
from players.player import Player
import numpy as np
import random

from players.random_player import RandomPlayer

class RandomLearningPlayer(Player):

    def __init__(self, color:DiscEnum, num_games:int = 100):
        super().__init__(color)

        print(f'Learning from {num_games} games.')

        self.custom_values = np.zeros((Board.SIZE, Board.SIZE), dtype=float)
        wins, losses, draws = self.play_games(num_games)

        print(f'Results: Wins: {wins}, losses: {losses}, draws: {draws}.')

    def play_games(self, num_games: int, exploration_rate: float = 0.5):
        wins = 0
        losses = 0
        draws = 0

        for i in range(num_games):
            # Initialize the game board
            board = Board(Board.SIZE)

            # Create a random bot as the opponent
            opponent_color = DiscEnum.BLACK if self.color == DiscEnum.WHITE else DiscEnum.WHITE
            opponent = RandomPlayer(opponent_color)  

            while not board.is_game_over():
                legal_moves = board.get_all_playable_points(self.color)

                if legal_moves:
                    if random.random() < exploration_rate * ((num_games - i)/num_games):
                        # Explore: Randomly select a move
                        move = random.choice(legal_moves)
                    else:
                        # Exploit: Select the move with the highest custom value
                        move = self.select_best_move(legal_moves)

                    # Make the move on the board for the RandomLearningPlayer
                    board.can_place_disc_and_flip(move, self.color)

                # Make the move for the opponent (RandomPlayer)
                legal_moves = board.get_all_playable_points(opponent.color)

                if legal_moves:
                    opponent_move = opponent.play(board)
                    board.can_place_disc_and_flip(opponent_move, opponent.color)

            # Evaluate the game outcome and update custom values
            outcome = board.winner_heuristic(self.color)
            self.evaluate_and_update(board, outcome)

            if outcome == 0:
                draws += 1
            elif outcome == -1:
                losses += 1
            else:
                wins += 1

        return wins, losses, draws

    def evaluate_and_update(self, board, outcome):
        for x in range(Board.SIZE):
            for y in range(Board.SIZE):
                if board.grid[y][x] == self.color.value:
                    # Increase the value for squares where the random player placed discs
                    self.custom_values[y][x] += outcome
                elif board.grid[y][x] != DiscEnum.EMPTY.value:
                    # Decrease the value for squares where the opponent placed discs
                    self.custom_values[y][x] -= outcome

    def select_best_move(self, legal_moves):
        best_move = None
        best_value = -float("inf")

        for move in legal_moves:
            x, y = move.x, move.y
            if self.custom_values[y][x] > best_value:
                best_move = move
                best_value = self.custom_values[y][x]

        return best_move

    def play(self, board: Board) -> Point:
        # Get all legal moves for the current player
        legal_moves = board.get_all_playable_points(self.color)

        if not legal_moves:
            return None  # No legal moves available

        # Choose the best move based on custom values
        best_move = self.select_best_move(legal_moves)

        return best_move
