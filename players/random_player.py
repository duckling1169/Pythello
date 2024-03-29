from game.enums import Color
from game.board import Board
from game.point import Point
from players.player import Player
import random

class RandomPlayer(Player):

    def __init__(self, color: Color):
        super().__init__(color)

    def play(self, board: Board) -> Point:
        return random.choice(board.get_legal_moves(self.color))
    