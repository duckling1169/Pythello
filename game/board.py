from game.enums import DiscEnum
from game.point import Point

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

    def is_game_over(self) -> bool:
        black_points = self.get_all_playable_points(DiscEnum.BLACK)
        white_points = self.get_all_playable_points(DiscEnum.WHITE)
        return not any(black_points) and not any(white_points)

    def is_point_in_bounds(self, point:Point):
        return point.x < len(self.grid) and point.x > -1 and point.y < len(self.grid) and point.y > -1

    def can_place_disc_and_flip(self, point:Point, color:DiscEnum, perform_flip:bool=True):
        if self.grid[point.y][point.x] != DiscEnum.EMPTY.value:
            return []

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
            return []
        
        # Place the disc and perform flips
        if perform_flip:
            self.grid[point.y][point.x] = color.value

            for path in flipped_discs:
                for point in path:
                    self.grid[point.y][point.x] = color.value

        return flipped_discs

    def get_all_playable_points(self, color: DiscEnum) -> [Point]:
        return [Point(x, y) for x in range(len(self.grid)) \
                for y in range(len(self.grid[0])) \
                if self.can_place_disc_and_flip(Point(x, y), color, False)]

    def calculate_color_points(self, color):
        return sum(row.count(color.value) for row in self.grid)

    def get_empty_spots(self):
        return sum(1 for x in range(len(self.grid)) \
            for y in range(len(self.grid[0])) \
            if self.grid[y][x] == DiscEnum.EMPTY.value)

    def winner_heuristic(self, color:DiscEnum):
        black_points = self.calculate_color_points(DiscEnum.BLACK)
        white_points = self.calculate_color_points(DiscEnum.WHITE)

        if black_points == white_points:
            return 0
        
        winner = DiscEnum.BLACK if black_points > white_points else DiscEnum.WHITE
        return 1 if winner == color else -1

    def mobility_heuristic(self, player_color):
        player_legal_moves = self.get_all_playable_points(player_color)
        opponent_legal_moves = self.get_all_playable_points(
            DiscEnum.BLACK if player_color == DiscEnum.WHITE else DiscEnum.WHITE
        )
        return len(player_legal_moves) - len(opponent_legal_moves)

    def square_heuristic(self, color):
        # Assign values to the board positions (customize these values)
        corner_value = 10
        x_square_value = -5
        c_square_value = -2
        
        # Define the board positions
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        x_squares = [(1, 1), (1, 6), (6, 1), (6, 6)]
        c_squares = [(0, 1), (1, 0), (6, 0), (7, 1), (0, 6), (1, 7), (6, 7), (7, 6)]

        # Initialize the heuristic value
        heuristic_value = 0

        # Iterate through each board position and assign custom values based on the color
        for y in range(len(self.grid)):
            for x in range(len(self.grid)):
                placed_color = self.grid[x][y]
                position = (x, y)
                if placed_color == DiscEnum.EMPTY.value:
                    pass  # You can add more custom logic for empty positions if needed
                mod = 1 if placed_color == color.value else -1
                if position in corners:
                    heuristic_value += corner_value * mod
                elif position in x_squares:
                    heuristic_value += x_square_value * mod
                elif position in c_squares:
                    heuristic_value += c_square_value * mod

        return heuristic_value
    
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
