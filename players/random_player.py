from players.player import Player
from game.enums import DiscEnum
from game.board import Board
from game.point import Point
import random

class RandomPlayer(Player):

    def __init__(self, color:DiscEnum):
        super().__init__(color)

    def play(self, board:Board) -> Point:
        return random.choice(board.get_all_playable_points(self.color))
    