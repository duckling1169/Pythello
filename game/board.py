from game.point import Point
from game.enums import Color

class Board():

    STARTING_POINTS = {
        Color.BLACK: [Point(3, 3), Point(4, 4)],
        Color.WHITE: [Point(3, 4), Point(4, 3)]
    }
    
    SIZE = 8

    def __init__(self, scale:int = 1):
        self.scale = scale

        self.grid = [[Color.EMPTY.value] * Board.SIZE for _ in range(Board.SIZE)]

        for color, points in Board.STARTING_POINTS.items():
            for point in points:
                self.grid[point.y][point.x] = color.value

# BOOLEANS
    def is_game_over(self) -> bool:
        """
        Check if the game is over.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        black_legal_moves = self.get_legal_moves(Color.BLACK)
        white_legal_moves = self.get_legal_moves(Color.WHITE)
        return not any(black_legal_moves) and not any(white_legal_moves)

    def is_valid_position(self, point) -> bool:
        """
        Check if a point is within the valid board boundaries.

        Args:
            point (Point): The point to be checked.

        Returns:
            bool: True if the point is within the valid board boundaries, False otherwise.
        """
        return 0 <= point.x < self.SIZE and 0 <= point.y < self.SIZE

    def is_stable_piece(self, point:Point, color:Color) -> bool:
        """
        Check if a piece at the specified point is stable for the given color.

        A piece is considered stable if it is surrounded by walls or pieces of the same color in at least four unique directions.

        Args:
            point (Point): The point to check for stability.
            color (Color): The color of the piece to be checked for stability.

        Returns:
            bool: True if the piece is stable, False otherwise.
        """
        if self.grid[point.y][point.x] != color.value:
            return False

        # Define the eight unique directions as Points
        directions = [Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1),
                    Point(1, 1), Point(-1, -1), Point(1, -1), Point(-1, 1)]

        # Count of unique directions where the piece is located
        unique_directions = set()  # Use a set to store unique directions
        color = self.grid[point.y][point.x]

        for direction in directions:
            current_point = point.__copy__()

            # Flag to track if the piece is stable in this direction
            is_stable = True

            walls = 0
            want_opposite_color = True
            while self.is_valid_position(current_point):
                current_color = self.grid[current_point.y][current_point.x]

                if current_color == Color.EMPTY.value:
                    walls -= 1
                    if walls == -1:
                        is_stable = False  # An empty square makes it not stable
                        break

                if want_opposite_color and current_color != color: # - - W B - - 
                    walls += 1
                    want_opposite_color = True

                if not want_opposite_color and current_point == color: # - - W B W - - -
                    walls += 1
                    want_opposite_color = False

                current_point.shift(direction.x, direction.y)

            if is_stable:
                # Check if the direction or its mirrored version is already in the set
                mirrored_direction = Point(-direction.x, -direction.y)
                if direction not in unique_directions and mirrored_direction not in unique_directions:
                    unique_directions.add(direction)

        # Check if the piece is at the end of at least four unique directions
        if len(unique_directions) == 4:
            return True

        return False

# HELPERS

    def get_legal_moves(self, color: Color) -> [Point]:
        return [Point(x, y) for x in range(Board.SIZE) \
                for y in range(Board.SIZE) \
                if self.place_and_flip_discs(Point(x, y), color, False)]

    def place_and_flip_discs(self, point:Point, color:Color, perform_flip:bool = True) -> [Point]:
        if self.grid[point.y][point.x] != Color.EMPTY.value:
            return []

        def flip_discs_in_direction(dx, dy):
            x, y = point.x + dx, point.y + dy
            flipped_discs = []

            while self.is_valid_position(Point(x, y)):
                if self.grid[y][x] == Color.EMPTY.value:
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

    def get_points_for_color(self, color:Color) -> int:
        return sum(row.count(color.value) for row in self.grid)

    def get_closest_corner(self, point: Point) -> Point:
        # Define the coordinates of the four corners
        corners = [Point(0, 0), Point(0, 7), Point(7, 0), Point(7, 7)]
        
        # Initialize variables to store the closest corner and its distance
        closest_corner = None
        closest_distance = float('inf')  # Initialize with positive infinity
        
        # Calculate the distance from the given point to each corner
        for corner in corners:
            distance = Point.dist(point.x, point.y, corner.x, corner.y)
            if distance < closest_distance:
                closest_distance = distance
                closest_corner = corner
        
        return closest_corner
    
# HEURISTICS

    def winner_heuristic(self, color: Color) -> int:
        """
        Calculate the winner heuristic for the specified color.

        The winner heuristic determines the outcome of the game based on the total number of points for each color.

        Args:
            color (Color): The color for which the winner heuristic is calculated.

        Returns:
            int: The winner heuristic score.
        """
        # Get the total number of points for both colors
        black_points = self.get_points_for_color(Color.BLACK)
        white_points = self.get_points_for_color(Color.WHITE)

        # Determine the winner based on the total points
        if black_points == white_points:
            return 0
        
        winner = Color.BLACK if black_points > white_points else Color.WHITE

        # Assign a score based on whether the color is the winner or not
        return 1 if winner == color else -1

    def mobility_heuristic(self, color: Color) -> int:
        """
        Calculate the mobility heuristic for the specified color.

        The mobility heuristic measures the difference in the number of legal moves between the player and the opponent.

        Args:
            color (Color): The color for which the mobility heuristic is calculated.

        Returns:
            int: The mobility heuristic score.
        """
        # Get the legal moves for the player and the opponent
        player_legal_moves = self.get_legal_moves(color)
        opponent_color = Color.BLACK if color == Color.WHITE else Color.WHITE
        opponent_legal_moves = self.get_legal_moves(opponent_color)

        # Calculate the difference in the number of legal moves
        mobility_score = len(player_legal_moves) - len(opponent_legal_moves)

        return mobility_score

    def square_heuristic(self, color:Color) -> int:
        """
        Calculate the square heuristic for the specified color.

        The square heuristic assigns values to different board positions based on their proximity to special squares and the color of the pieces.

        Args:
            color (Color): The color for which the square heuristic is calculated.

        Returns:
            int: The square heuristic score.
        """
        # Assign values to the board positions 
        corner_value = 10
        c_square_value = -5
        x_square_value = -2

        # Define the board positions
        corners = [Point(0, 0), Point(0, 7), Point(7, 0), Point(7, 7)]
        c_squares = [Point(1, 1), Point(1, 6), Point(6, 1), Point(6, 6)]
        x_squares = [Point(0, 1), Point(1, 0), Point(6, 0), Point(0, 6), Point(7, 1), Point(1, 7), Point(6, 7), Point(7, 6)]

        # Initialize the heuristic value
        heuristic_value = 0

        # Iterate through each board position and assign custom values based on the color
        for y in range(Board.SIZE):
            for x in range(Board.SIZE):
                placed_color = self.grid[y][x]
                if placed_color == Color.EMPTY.value:
                    continue 

                point = Point(x,y)
                mod = 1 if placed_color == color.value else -1

                closest_corner = self.get_closest_corner(point)
                corner_color = self.grid[closest_corner.y][closest_corner.x]

                if corner_color == color.value: # everything should be positive
                    if point in corners:
                        heuristic_value += corner_value * 1  # Highly value corner
                    elif point in c_squares:                            
                        heuristic_value += 0 # c_square_value * -1  # Devalue c-square
                    elif point in x_squares:
                        heuristic_value += 0 # x_square_value * -1  # Devalue x-square
                else:
                    if point in corners:
                        heuristic_value += corner_value * mod  # Highly value corner
                    elif point in c_squares:
                        heuristic_value += c_square_value * mod  # Devalue c-square
                    elif point in x_squares:
                        heuristic_value += x_square_value * mod  # Devalue x-square

        return heuristic_value

    def stability_heuristic(self, color: Color) -> int:
        """
        Calculate the stability heuristic for the specified color.

        The stability heuristic represents the number of stable pieces for the given color on the board.

        Args:
            color (Color): The color for which stability is calculated.

        Returns:
            int: The stability heuristic score.
        """
        stability_heuristic = sum(1 for y in range(Board.SIZE) for x in range(Board.SIZE) if self.is_stable_piece(Point(y, x), color))
        return stability_heuristic

    def __str__(self):
        scale = self.scale
        grid = self.grid
        
        # Determine the number of spaces for the header separator line
        spaces = 3 if len(grid) < 11 else 4
        s = '\n    '

        # Loop through each column index and add column numbers with appropriate spacing
        for i in range(len(grid)):
            s += '  ' * self.scale + chr(ord('a') + i)

        # Print separator below letter row
        s += '\n' + ' ' * spaces + '+' + f"{'--' * scale}+" * len(grid) + '\n'
        
        # Loop through each row in the grid, starting from the bottom
        for i in range(1, len(grid)*scale + 1):
            num = i // scale
            if i % scale == 0:
                # Add row number with appropriate spacing
                s += f"{num:2d} |" + '  ' * scale

                # Join the elements in the row as strings with spacing and add newlines
                s += ('  ' * scale).join(map(str, grid[int(i/scale)-1])) + '\n'
            else:
                s += '   |\n'

        return s
