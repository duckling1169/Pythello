from game.point import Point
from game.enums import DiscEnum

class Disc(Point):

    def __init__(self, x:int, y:int, color:DiscEnum):
        self.color = color
        super().__init__(x, y)

    def __str__(self):
        return f'{self.color.name.title()} disc at ({(self.x)}, {self.y})'
