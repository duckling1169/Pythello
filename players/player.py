from game.board import Board
from game.enums import Color
from game.point import Point

class Player:
    """
    Represents a player in a game.
    """

    def __init__(self, color: Color):
        """
        Initialize a player with the given color.

        Args:
            color (Color): The color of the player.
        """
        self.color = color
        self.score = 2

    def play(self, board: Board) -> Point:
        """
        Get the player's move.

        Args:
            board (Board): The current game board.

        Returns:
            Point: The point representing the player's move.
        """
        while True:
            resp = input(f'Placement: ')
            try:
                x = ord(resp.split(',')[0]) - ord('a')
                y = int(resp.split(',')[1]) - 1
                move = Point(x, y)
                if move in board.get_legal_moves(self.color):
                    return move
            except:
                continue

    def __str__(self):
        """
        Get a string representation of the player.

        Returns:
            str: A string describing the player's color and type.
        """
        return f'{type(self).__name__} ({self.color.name.title()}, {self.color.value})'
