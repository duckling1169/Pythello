from game.enums import DiscEnum
from game.board import Board
from game.point import Point

class Player:

    def __init__(self, color:DiscEnum):
        self.color = color
        self.score = 2

    def play(self, board:Board) -> Point:
        while True:
            resp = input(f'Placement: ')
            try:
                x = int(resp.split(',')[0])
                y = int(resp.split(',')[1])
                return Point(x, y)
            except:
                continue
            
    def __str__(self):
        return f'{type(self).__name__} ({self.color.name.title()}, {self.color.value})'
            