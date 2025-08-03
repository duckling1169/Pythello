import pytest
from unittest.mock import Mock, patch
from game.board import Board
from game.enums import Color
from game.point import Point
from players.player import Player
from players.random_player import RandomPlayer
from players.minimax_player import MiniMaxPlayer
from players.mcts_player import MCTSPlayer, MCTSNode
from players.heuristics_players import HeuristicPlayer


class TestRandomPlayer:
    """Test cases for RandomPlayer."""

    def test_random_player_initialization(self):
        """Test random player initialization."""
        player = RandomPlayer(Color.BLACK)
        assert player.color == Color.BLACK
        assert player.score == 2

    def test_random_player_play(self):
        """Test random player move selection."""
        board = Board()
        player = RandomPlayer(Color.BLACK)
        
        move = player.play(board)
        legal_moves = board.get_legal_moves(Color.BLACK)
        
        assert move in legal_moves

    def test_random_player_string_representation(self):
        """Test random player string representation."""
        player = RandomPlayer(Color.BLACK)
        player_str = str(player)
        
        assert "RandomPlayer" in player_str
        assert "Black" in player_str


class TestMiniMaxPlayer:
    """Test cases for MiniMaxPlayer."""

    def test_minimax_player_initialization(self):
        """Test minimax player initialization."""
        player = MiniMaxPlayer(Color.BLACK, ['square_heuristic'], max_depth=3)
        
        assert player.color == Color.BLACK
        assert player.max_depth == 3
        assert len(player.heuristics) == 1
        assert 'square_heuristic' in player.heuristic_names

    def test_minimax_player_play(self):
        """Test minimax player move selection."""
        board = Board()
        player = MiniMaxPlayer(Color.BLACK, ['square_heuristic'], max_depth=2)
        
        move = player.play(board)
        legal_moves = board.get_legal_moves(Color.BLACK)
        
        assert move in legal_moves

    def test_minimax_with_heuristics_depth_zero(self):
        """Test minimax at depth zero."""
        board = Board()
        player = MiniMaxPlayer(Color.BLACK, ['mobility_heuristic'], max_depth=1)
        
        move, score = player.minimax_with_heuristics(board, Color.BLACK, 0, player.heuristics)
        
        assert move is None
        assert isinstance(score, (int, float))

    def test_minimax_game_over(self):
        """Test minimax when game is over."""
        board = Board()
        # Fill board to force game over
        for x in range(Board.SIZE):
            for y in range(Board.SIZE):
                board.grid[y][x] = Color.BLACK.value
        
        player = MiniMaxPlayer(Color.BLACK, ['mobility_heuristic'], max_depth=2)
        move, score = player.minimax_with_heuristics(board, Color.BLACK, 1, player.heuristics)
        
        assert move is None
        assert score == 100  # Black wins


class TestMCTSPlayer:
    """Test cases for MCTSPlayer."""

    def test_mcts_player_initialization(self):
        """Test MCTS player initialization."""
        player = MCTSPlayer(Color.BLACK, iterations=100)
        
        assert player.color == Color.BLACK
        assert player.iterations == 100

    def test_mcts_player_play(self):
        """Test MCTS player move selection."""
        board = Board()
        player = MCTSPlayer(Color.BLACK, iterations=10)  # Low iterations for speed
        
        move = player.play(board)
        legal_moves = board.get_legal_moves(Color.BLACK)
        
        assert move in legal_moves

    def test_mcts_node_initialization(self):
        """Test MCTS node initialization."""
        board = Board()
        node = MCTSNode(board, Color.BLACK, Point(2, 3))
        
        assert node.color == Color.BLACK
        assert node.move == Point(2, 3)
        assert node.visits == 0
        assert node.value == 0
        assert node.parent is None
        assert len(node.children) == 0

    def test_mcts_simulate(self):
        """Test MCTS simulation."""
        board = Board()
        player = MCTSPlayer(Color.BLACK, iterations=10)
        node = MCTSNode(board, Color.BLACK)
        
        score = player.simulate(node)
        assert isinstance(score, int)
        assert score in [-100, 0, 100]  # Should be a valid winner heuristic

    def test_mcts_backpropagate(self):
        """Test MCTS backpropagation."""
        board = Board()
        player = MCTSPlayer(Color.BLACK, iterations=10)
        
        root = MCTSNode(board, Color.BLACK)
        child = MCTSNode(board, Color.WHITE)
        child.parent = root
        
        player.backpropagate(child, 50)
        
        assert child.visits == 1
        assert child.value == -50  # Opponent move, so negative

    def test_mcts_select_best_move(self):
        """Test MCTS best move selection."""
        board = Board()
        player = MCTSPlayer(Color.BLACK, iterations=10)
        root = MCTSNode(board, Color.BLACK)
        
        # Add some children with different values
        child1 = MCTSNode(board, Color.WHITE, Point(2, 3))
        child1.visits = 10
        child1.value = 30
        
        child2 = MCTSNode(board, Color.WHITE, Point(3, 2))
        child2.visits = 5
        child2.value = 20
        
        root.children = [child1, child2]
        
        best_move = player.select_best_move(root)
        assert best_move == Point(2, 3)  # Higher average value


class TestHeuristicPlayer:
    """Test cases for HeuristicPlayer."""

    def test_heuristic_player_initialization(self):
        """Test heuristic player initialization."""
        player = HeuristicPlayer(Color.BLACK, ['mobility_heuristic', 'square_heuristic'])
        
        assert player.color == Color.BLACK
        assert len(player.heuristics) == 2

    def test_heuristic_player_play(self):
        """Test heuristic player move selection."""
        board = Board()
        player = HeuristicPlayer(Color.BLACK, ['mobility_heuristic'])
        
        move = player.play(board)
        legal_moves = board.get_legal_moves(Color.BLACK)
        
        assert move in legal_moves

    def test_heuristic_player_invalid_heuristic(self):
        """Test heuristic player with invalid heuristic."""
        player = HeuristicPlayer(Color.BLACK, ['invalid_heuristic'])
        
        # Should have None for invalid heuristic
        assert None in player.heuristics