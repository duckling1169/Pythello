from game.enums import DiscEnum
from game.board import Board
from game.point import Point

class Player:

    def __init__(self, color:DiscEnum):
        self.color = color

    def play(self, board:Board) -> Point:
        while True:
            resp = input(f'Your turn! (x,y)\n')
            if resp == 'q':
                return None
            try:
                x = int(resp.split(',')[0])
                y = int(resp.split(',')[1])
                return Point(x, y)
            except:
                continue
            

            