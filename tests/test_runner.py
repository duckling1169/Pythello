import pytest
from unittest.mock import Mock, patch
from runner import Runner
from game.board import Board
from game.enums import Color
from players.random_player import RandomPlayer
from players.minimax_player import MiniMaxPlayer


class TestRunner:
    """Test cases for the Runner class."""

    def test_play_game_basic(self):
        """Test basic game play between two players."""
        player1 = RandomPlayer(Color.BLACK)
        player2 = RandomPlayer(Color.WHITE)
        
        winner = Runner.play_game([player1, player2], show_game=False)
        
        # Winner should be one of the players or None (tie)
        assert winner in [player1, player2, None]
        
        # Both players should have scores set
        assert hasattr(player1, 'score')
        assert hasattr(player2, 'score')

    def test_play_game_with_display(self):
        """Test game play with display enabled."""
        player1 = RandomPlayer(Color.BLACK)
        player2 = RandomPlayer(Color.WHITE)
        
        with patch('builtins.print'):  # Mock print to avoid output during tests
            winner = Runner.play_game([player1, player2], show_game=True)
        
        assert winner in [player1, player2, None]

    def test_compare_players(self):
        """Test player comparison functionality."""
        player1 = RandomPlayer(Color.BLACK)
        player2 = RandomPlayer(Color.WHITE)
        
        with patch('builtins.print'):  # Mock print to avoid output during tests
            result = Runner.compare_players(player1, player2, games=2, show_game=False)
        
        assert result is True

    def test_compare_players_with_display(self):
        """Test player comparison with display enabled."""
        player1 = RandomPlayer(Color.BLACK)
        player2 = RandomPlayer(Color.WHITE)
        
        with patch('builtins.print'):  # Mock print to avoid output during tests
            result = Runner.compare_players(player1, player2, games=1, show_game=True)
        
        assert result is True

    def test_compare_players_break_at_loss(self):
        """Test player comparison with break_at_loss option."""
        player1 = RandomPlayer(Color.BLACK)
        player2 = RandomPlayer(Color.WHITE)
        
        with patch('builtins.print'):  # Mock print to avoid output during tests
            result = Runner.compare_players(player1, player2, games=10, break_at_loss=True)
        
        assert result is True

    def test_play_game_invalid_move_handling(self):
        """Test that invalid moves are handled correctly."""
        
        class InvalidMovePlayer(RandomPlayer):
            def __init__(self, color):
                super().__init__(color)
                self.invalid_moves_returned = 0
                
            def play(self, board):
                # Return invalid move first few times
                if self.invalid_moves_returned < 2:
                    self.invalid_moves_returned += 1
                    return Point(0, 0)  # Usually invalid
                return super().play(board)
        
        # Import Point for the test
        from game.point import Point
        
        player1 = InvalidMovePlayer(Color.BLACK)
        player2 = RandomPlayer(Color.WHITE)
        
        with patch('builtins.print'):  # Mock print to avoid output during tests
            winner = Runner.play_game([player1, player2], show_game=True)
        
        assert winner in [player1, player2, None]

    def test_game_completion(self):
        """Test that games complete properly."""
        player1 = RandomPlayer(Color.BLACK)
        player2 = RandomPlayer(Color.WHITE)
        
        # Run multiple games to ensure they complete
        for _ in range(3):
            winner = Runner.play_game([player1, player2])
            assert winner in [player1, player2, None]
            
            # Reset player scores for next game
            player1.score = 2
            player2.score = 2