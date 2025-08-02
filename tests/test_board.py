import pytest
from game.board import Board
from game.enums import Color
from game.point import Point


class TestBoard:
    """Test cases for the Board class."""

    def test_board_initialization(self):
        """Test board initialization with correct starting positions."""
        board = Board()
        
        # Check starting positions
        assert board.grid[3][3] == Color.BLACK.value
        assert board.grid[4][4] == Color.BLACK.value
        assert board.grid[3][4] == Color.WHITE.value
        assert board.grid[4][3] == Color.WHITE.value
        
        # Check board size
        assert len(board.grid) == Board.SIZE
        assert len(board.grid[0]) == Board.SIZE
        
        # Check scale
        assert board.scale == 1

    def test_board_initialization_with_scale(self):
        """Test board initialization with custom scale."""
        board = Board(scale=2)
        assert board.scale == 2

    def test_is_valid_position(self):
        """Test position validation."""
        board = Board()
        
        # Valid positions
        assert board.is_valid_position(Point(0, 0))
        assert board.is_valid_position(Point(7, 7))
        assert board.is_valid_position(Point(3, 4))
        
        # Invalid positions
        assert not board.is_valid_position(Point(-1, 0))
        assert not board.is_valid_position(Point(0, -1))
        assert not board.is_valid_position(Point(8, 0))
        assert not board.is_valid_position(Point(0, 8))

    def test_get_legal_moves_initial(self):
        """Test getting legal moves from initial position."""
        board = Board()
        
        black_moves = board.get_legal_moves(Color.BLACK)
        expected_black = [Point(2, 3), Point(3, 2), Point(4, 5), Point(5, 4)]
        
        assert len(black_moves) == 4
        for move in expected_black:
            assert move in black_moves

    def test_is_legal_move(self):
        """Test individual legal move checking."""
        board = Board()
        
        # Legal moves for black
        assert board.is_legal_move(Point(2, 3), Color.BLACK)
        assert board.is_legal_move(Point(3, 2), Color.BLACK)
        
        # Illegal moves
        assert not board.is_legal_move(Point(3, 3), Color.BLACK)  # Occupied
        assert not board.is_legal_move(Point(0, 0), Color.BLACK)  # No flips possible

    def test_place_and_flip_discs(self):
        """Test placing discs and flipping opponent discs."""
        board = Board()
        
        # Place a black disc
        flipped = board.place_and_flip_discs(Point(2, 3), Color.BLACK)
        
        # Check the move was placed
        assert board.grid[3][2] == Color.BLACK.value
        
        # Check a disc was flipped
        assert len(flipped) > 0
        assert board.grid[3][3] == Color.BLACK.value

    def test_place_and_flip_discs_dry_run(self):
        """Test place_and_flip_discs in dry run mode."""
        board = Board()
        
        # Dry run should return flipped discs but not modify board
        original_grid = [row[:] for row in board.grid]
        flipped = board.place_and_flip_discs(Point(2, 3), Color.BLACK, perform_flip=False)
        
        # Board should be unchanged
        assert board.grid == original_grid
        
        # But should return what would be flipped
        assert len(flipped) > 0

    def test_get_points_for_color(self):
        """Test counting points for each color."""
        board = Board()
        
        # Initial position has 2 pieces each
        assert board.get_points_for_color(Color.BLACK) == 2
        assert board.get_points_for_color(Color.WHITE) == 2

    def test_is_game_over(self):
        """Test game over detection."""
        board = Board()
        
        # Game should not be over initially
        assert not board.is_game_over()
        
        # Fill board to force game over
        for x in range(Board.SIZE):
            for y in range(Board.SIZE):
                board.grid[y][x] = Color.BLACK.value
        
        assert board.is_game_over()

    def test_winner_heuristic(self):
        """Test winner heuristic calculation."""
        board = Board()
        
        # Game not over should return 0
        assert board.winner_heuristic(Color.BLACK) == 0
        
        # Create a game over state with black winning
        for x in range(Board.SIZE):
            for y in range(Board.SIZE):
                board.grid[y][x] = Color.BLACK.value
        
        assert board.winner_heuristic(Color.BLACK) == 100
        assert board.winner_heuristic(Color.WHITE) == -100

    def test_mobility_heuristic(self):
        """Test mobility heuristic calculation."""
        board = Board()
        
        # Initially should have same mobility
        mobility = board.mobility_heuristic(Color.BLACK)
        # Black has 4 moves, white has 4 moves initially
        assert mobility == 0

    def test_points_heuristic(self):
        """Test points heuristic calculation."""
        board = Board()
        
        # Initially should be 0 (2-2 = 0)
        assert board.points_heuristic(Color.BLACK) == 0

    def test_square_heuristic(self):
        """Test square heuristic calculation."""
        board = Board()
        
        # Place piece in corner
        board.grid[0][0] = Color.BLACK.value
        board.grid[3][3] = Color.EMPTY.value  # Remove starting piece
        
        heuristic = board.square_heuristic(Color.BLACK)
        assert heuristic > 0  # Should be positive for corner

    def test_stability_heuristic(self):
        """Test stability heuristic calculation."""
        board = Board()
        
        # Fill entire board with black
        for x in range(Board.SIZE):
            for y in range(Board.SIZE):
                board.grid[y][x] = Color.BLACK.value
        
        stability = board.stability_heuristic(Color.BLACK)
        assert stability > 0

    def test_get_closest_corner(self):
        """Test finding closest corner."""
        board = Board()
        
        assert board.get_closest_corner(Point(1, 1)) == Point(0, 0)
        assert board.get_closest_corner(Point(6, 6)) == Point(7, 7)
        assert board.get_closest_corner(Point(1, 6)) == Point(0, 7)
        assert board.get_closest_corner(Point(6, 1)) == Point(7, 0)

    def test_is_stable_piece(self):
        """Test stability piece detection."""
        board = Board()
        
        # Corner piece should be stable when surrounded
        board.grid[0][0] = Color.BLACK.value
        board.grid[0][1] = Color.BLACK.value
        board.grid[1][0] = Color.BLACK.value
        board.grid[1][1] = Color.BLACK.value
        
        # Fill more to make it truly stable
        for i in range(Board.SIZE):
            board.grid[0][i] = Color.BLACK.value
            board.grid[i][0] = Color.BLACK.value
        
        assert board.is_stable_piece(Point(0, 0), Color.BLACK)

    def test_board_string_representation(self):
        """Test board string output."""
        board = Board()
        board_str = str(board)
        
        # Should contain letters and numbers
        assert 'a' in board_str
        assert '1' in board_str
        
        # Should contain the starting pieces
        assert 'X' in board_str  # Black pieces
        assert 'O' in board_str  # White pieces