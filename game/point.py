import math

class Point:

    def __init__(self, x_init: int, y_init: int):
        self.x = x_init
        self.y = y_init

    def shift(self, x: int, y: int) -> None:
        self.x += x
        self.y += y

    @staticmethod
    def dist(p1_x: int, p1_y: int, p2_x: int, p2_y: int) -> float:
        return round(math.dist([p1_x, p1_y], [p2_x, p2_y]), 2)

    def __copy__(self):
        return Point(self.x, self.y)
    
    def __eq__(self, obj):
        return isinstance(obj, Point) and obj.x == self.x and obj.y == self.y
    
    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f'({chr(ord("a") + self.x)}, {self.y + 1})'