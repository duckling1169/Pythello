from game.point import Point
from game.disc import Disc
from game.enums import DiscEnum

class Board():

    STARTING_POINTS = {
        DiscEnum.BLACK: [Point(3, 3), Point(4, 4)],
        DiscEnum.WHITE: [Point(3, 4), Point(4, 3)]
    }
    
    SIZE = 8

    def __init__(self, size, scale:int=1):
        self.scale = scale

        self.grid = [[DiscEnum.EMPTY.value] * size for _ in range(size)]

        for color, points in Board.STARTING_POINTS.items():
            for point in points:
                self.grid[point.y][point.x] = color.value
    
    def can_place_disc_and_flip(self, point:Point, color:DiscEnum, perform_flip:bool=True):
        if self.grid[point.y][point.x] != DiscEnum.EMPTY.value:
            return False

        def flip_discs_in_direction(dx, dy):
            x, y = point.x + dx, point.y + dy
            flipped_discs = []

            while self.is_point_in_bounds(Point(x, y)):
                if self.grid[y][x] == DiscEnum.EMPTY.value:
                    return []

                if self.grid[y][x] == color.value:
                    return flipped_discs

                flipped_discs.append(Point(x, y))
                x += dx
                y += dy

            return []

        # Define directions for all 8 possible neighbors
        directions = [Point(-1, 0), Point(-1, 1), Point(0, 1), Point(1, 1), Point(1, 0), Point(1, -1), Point(0, -1), Point(-1, -1)]

        flipped_discs = []

        # Check directions and assign results to `disc` simultaneously
        flipped_discs = [disc for direction in directions if (disc := flip_discs_in_direction(direction.x, direction.y))]

        if not flipped_discs:
            return False
        
        # Place the disc and perform flips
        if perform_flip:
            self.grid[point.y][point.x] = color.value

            for path in flipped_discs:
                for point in path:
                    self.grid[point.y][point.x] = color.value

        return True

    def is_point_in_bounds(self, point:Point):
        return point.x < len(self.grid) and point.x > -1 and point.y < len(self.grid) and point.y > -1

    def get_all_playable_points(self, color: DiscEnum) -> [Point]:
        return [Point(x, y) for x in range(len(self.grid)) \
                for y in range(len(self.grid[0])) \
                if self.can_place_disc_and_flip(Point(x, y), color, False)]

    def calculate_player_points(self, player):
        return sum(row.count(player.color.value) for row in self.grid)

    def __str__(self):
        scale = self.scale
        grid = self.grid
        s = '\n'

        # Loop through each row in the grid, starting from the bottom
        for i in range(len(grid)*scale - 1, -1, -1):
            if (i+1) % scale == 0:
                # Add row number with appropriate spacing
                s += f"{(int)(i/scale):2d} |" + '  ' * scale
                # Join the elements in the row as strings with spacing and add newlines
                s += ('  ' * scale).join(map(str, grid[(int)(i/scale)])) + '\n'
            else:
                s += '   |\n'
        
        # Determine the number of spaces for the header separator line
        spaces = 3 if len(grid) < 11 else 4
        # Add the header separator line
        s += ' ' * spaces + '+' + f"{'--' * scale}+" * len(grid) + '\n' + ' ' * 4
        
        # Loop through each column index and add column numbers with appropriate spacing
        for c in range(len(grid)):
            s += '  ' * self.scale + str(c)

        return s
