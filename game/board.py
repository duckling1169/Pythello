from game.point import Point
from game.enums import Color
from typing import List
from math import ceil
class Board():

    STARTING_POINTS = {
        Color.BLACK: [Point(3, 3), Point(4, 4)],
        Color.WHITE: [Point(3, 4), Point(4, 3)]
    }
    
    SIZE: int = 8

    def __init__(self, scale: int = 1):
        self.scale = scale

        self.grid: List[List[str]] = [[Color.EMPTY.value] * Board.SIZE for _ in range(Board.SIZE)]

        for color, points in Board.STARTING_POINTS.items():
            for point in points:
                self.grid[point.y][point.x] = color.value

    def is_game_over(self) -> bool:
        """
        Check if the game is over.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        black_legal_moves = self.get_legal_moves(Color.BLACK)
        white_legal_moves = self.get_legal_moves(Color.WHITE)
        return not any(black_legal_moves) and not any(white_legal_moves)

    def is_valid_position(self, point: Point) -> bool:
        """
        Check if a point is within the valid board boundaries.

        Args:
            point (Point): The point to be checked.

        Returns:
            bool: True if the point is within the valid board boundaries, False otherwise.
        """
        return 0 <= point.x < self.SIZE and 0 <= point.y < self.SIZE

    def is_stable_piece(self, point: Point, color: Color) -> bool:
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
        directions: List[Point] = [Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1),
                    Point(1, 1), Point(-1, -1), Point(1, -1), Point(-1, 1)]

        unique_directions: set = set()
       
        for direction in directions:
            current_point = point.__copy__()
            is_stable: bool = True # Flag to track if the piece is stable in this direction
            
            while self.is_valid_position(current_point):
                color_value = self.grid[current_point.y][current_point.x]

                if color_value == Color.EMPTY.value:
                    is_stable = False  # An empty square makes the space not stable
                    break

                current_point.shift(direction.x, direction.y)

            if is_stable: # Check if the direction or its mirrored version is already in the set
                mirrored_direction: Point = Point(-direction.x, -direction.y)
                if not (direction in unique_directions or mirrored_direction in unique_directions):
                    unique_directions.add(direction)

        # Check if the piece is at the end of at least four unique directions
        if len(unique_directions) == 4:
            return True

        return False

    def get_legal_moves(self, color: Color) -> List[Point]:
        return [Point(x, y) for x in range(Board.SIZE) \
                for y in range(Board.SIZE) \
                if self.place_and_flip_discs(Point(x, y), color, False)]

    def place_and_flip_discs(self, point: Point, color: Color, perform_flip: bool = True) -> List[Point]:
        if self.grid[point.y][point.x] != Color.EMPTY.value:
            return []

        def flip_discs_in_direction(dx: int, dy: int) -> List[Point]:
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
        directions: List[Point] = [Point(-1, 0), Point(-1, 1), Point(0, 1), Point(1, 1), Point(1, 0), Point(1, -1), Point(0, -1), Point(-1, -1)]

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

    def get_points_for_color(self, color: Color) -> int:
        return sum(row.count(color.value) for row in self.grid)

    def get_closest_corner(self, point: Point) -> Point:
        # Define the coordinates of the four corners
        corners: List[Point] = [Point(0, 0), Point(0, 7), Point(7, 0), Point(7, 7)]
        closest_corner: Point = None
        closest_distance = float('inf')
        
        # Calculate the distance from the given point to each corner
        for corner in corners:
            distance = Point.dist(point.x, point.y, corner.x, corner.y)
            if distance < closest_distance:
                closest_distance = distance
                closest_corner = corner
        
        return closest_corner

    def winner_heuristic(self, color: Color) -> int:
        """
        Calculate the winner heuristic for the specified color.

        The winner heuristic determines the outcome of the game based on the total number of points for each color.

        Args:
            color (Color): The color for which the winner heuristic is calculated.

        Returns:
            int: The winner heuristic score.
        """
        if not self.is_game_over():
            return 0
        
        # Get the total number of points for both colors
        black_points = self.get_points_for_color(Color.BLACK)
        white_points = self.get_points_for_color(Color.WHITE)

        # Determine the winner based on the total points
        if black_points == white_points:
            return 0
        
        winner = Color.BLACK if black_points > white_points else Color.WHITE

        # Assign a score based on whether the color is the winner or not
        return 100 if winner == color else -100

    def points_heuristic(self, color: Color, threshold: float = 0.7) -> int:
        """
        Calculate a heuristic value for the given player's position on the board.

        Args:
            color (Color): The color of the player for whom the heuristic is calculated.

        Returns:
            int: The heuristic value representing the difference in points between the player
                and their opponent. Positive values favor the player; negative values favor the opponent.
        """
        opponent_color = Color.BLACK if color == Color.WHITE else Color.WHITE
        player_points = self.get_points_for_color(color)
        opponent_points = self.get_points_for_color(opponent_color)

        maximize = threshold * Board.SIZE * Board.SIZE
        return player_points - opponent_points if (player_points + opponent_points) > maximize else opponent_points - player_points

    def mobility_heuristic(self, color: Color) -> int:
        """
        Calculate the mobility heuristic for the specified color.

        The mobility heuristic measures the difference in the number of legal moves between the player and the opponent.

        Args:
            color (Color): The color for which the mobility heuristic is calculated.

        Returns:
            int: The mobility heuristic score.
        """
        opponent_color = Color.BLACK if color == Color.WHITE else Color.WHITE

        # Get the legal moves for the player and the opponent
        player_legal_moves = self.get_legal_moves(color)
        opponent_legal_moves = self.get_legal_moves(opponent_color)

        # Calculate the difference in the number of legal moves
        return len(player_legal_moves) - len(opponent_legal_moves)

    def square_heuristic(self, color: Color) -> int:
        """
        Calculate the square heuristic for the specified color.

        The square heuristic assigns values to different board positions based on their proximity to special squares and the color of the pieces.

        Args:
            color (Color): The color for which the square heuristic is calculated.

        Returns:
            int: The square heuristic score.
        """
        CORNER_VALUE = 12
        C_SQUARE_VALUE = -7
        X_SQUARE_VALUE = -3
        
        corners: List[Point] = [Point(0, 0), Point(0, 7), Point(7, 0), Point(7, 7)]
        heuristic_value: int = 0

        for corner in corners:
            corner_color = self.grid[corner.y][corner.x]

            if corner_color != Color.EMPTY.value:
                heuristic_value += CORNER_VALUE * (1 if corner_color == color.value else -1)
                continue

            directions: List[Point] = [Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1),
                        Point(1, 1), Point(-1, -1), Point(1, -1), Point(-1, 1)]
            
            for direction in directions:
                point = corner.__copy__()
                point.shift(direction.x, direction.y)
                if not self.is_valid_position(point):
                    continue

                square_color = self.grid[point.y][point.x]
                if direction.x == 0 or direction.y == 0: # X SQUARE                    
                    if square_color != Color.EMPTY.value:
                        heuristic_value += X_SQUARE_VALUE * 1 if square_color == color.value else -1
                else: # C SQUARE
                    if square_color != Color.EMPTY.value:
                        heuristic_value += C_SQUARE_VALUE * 1 if square_color == color.value else -1

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
        POINTS = 3
        stability_heuristic = sum(POINTS for y in range(Board.SIZE) for x in range(Board.SIZE) if self.is_stable_piece(Point(y, x), color))
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
