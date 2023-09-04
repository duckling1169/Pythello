from game.point import Point
from game.enums import Color
from game.board import Board
from players.player import Player
import numpy as np
import random
import copy

from players.random_player import RandomPlayer

class RandomLearningPlayer(Player):

    def __init__(self, color: Color, num_games: int = 100):
        super().__init__(color)

        print(f'Learning from {num_games} games.')

        self.num_games = num_games
        self.game_boards = [[] for _ in range(num_games)]  # List to store boards for each game
        self.custom_values = np.zeros((Board.SIZE, Board.SIZE), dtype=float)
        wins, losses, draws = self.play_games()

        print(f'Results: Wins: {wins}, losses: {losses}, draws: {draws}.')

    def play_games(self):
        wins = 0
        losses = 0
        draws = 0

        for i in range(self.num_games):
            # Initialize the game board
            board = Board()

            # Create a random bot as the opponent
            opponent_color = Color.BLACK if self.color == Color.WHITE else Color.WHITE
            opponent = RandomPlayer(opponent_color)

            move_num = 0
            while not board.is_game_over():
                # Handle the RandomLearningPlayer's move
                self.handle_player_move(board, self.color, move_num)
                move_num += 1

                # Handle the opponent's move
                self.handle_player_move(board, opponent.color, move_num)
                move_num += 1

            # Evaluate the final game outcome and update wins, losses, and draws
            outcome = board.winner_heuristic(self.color)
            if outcome == 0:
                draws += 1
            elif outcome == -1:
                losses += 1
            else:
                wins += 1

        return wins, losses, draws

    def handle_player_move(self, board:Board, player_color:Color, move_num):
        legal_moves = board.get_legal_moves(player_color)

        if legal_moves:
            # Always select a random move during training
            move = random.choice(legal_moves)

            # Make a copy of the board before making the move
            board_copy = copy.deepcopy(board)
            board_copy.place_and_flip_discs(move, player_color)

            # Store the board for this move in the game_boards list
            self.game_boards[move_num].append(board_copy)

            # Make the move on the original board
            board.place_and_flip_discs(move, player_color)

    def select_best_move(self, board:Board, legal_moves):
        best_move = None
        best_value = -float("inf")

        for move in legal_moves:
            x, y = move.x, move.y
            if self.custom_values[y][x] > best_value:
                best_move = move
                best_value = self.custom_values[y][x]

        return best_move

    def play(self, board: Board) -> Point:
        
        b = [board for board in self.game_boards[0]]

        print(len(b))

        legal_moves = board.get_legal_moves(self.color)

        if not legal_moves:
            return None  # No legal moves available

        # Always select a random move during play
        return self.select_best_move(board, legal_moves)

