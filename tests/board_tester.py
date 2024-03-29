from game.board import Board
from game.enums import Color
from game.point import Point
from players.player import Player
from players.random_player import RandomPlayer
from players.minimax_player import MiniMaxPlayer
from players.heuristics_players import HeuristicPlayer

import copy
from time import perf_counter

class BoardTester:

    def __init__(self, player):
        func_list = [func for func in dir(BoardTester) if callable(getattr(BoardTester, func)) and 'test' in func ]
        print(f'BoardTester running {len(func_list)} tests.')
        for func in func_list:
            print(f'{func}: {getattr(BoardTester, func)(player)}')

    def test_scale(player:Player):
        board = Board(scale=2)
        return board.scale == 2

    def test_place_disc(player:Player):
        board = Board()
        res1 = any(board.place_and_flip_discs(Point(3, 2), Color.BLACK))
        res2 = any(board.place_and_flip_discs(Point(4, 2), Color.BLACK))
        return not res1 and res2

    def test_board_copy(player:Player):
        board = Board()
        board2 = copy.deepcopy(board)
        board.place_and_flip_discs(Point(3, 2), Color.BLACK)
        board2.place_and_flip_discs(Point(4, 2), Color.BLACK)
        return board != board2
    
    def test_all_playable_spots(player:Player):
        board = Board()
        points = board.get_legal_moves(Color.BLACK)
        board.place_and_flip_discs(points[0], Color.BLACK)
        points = board.get_legal_moves(Color.WHITE)
        return points == [Point(2,3), Point(2,5), Point(4,5)]

    def test_is_game_over(player:Player):
        board = Board()
        board2 = Board()
        board.grid = [[Color.BLACK.value] * len(board.grid) for _ in range(len(board.grid))]
        return board.is_game_over() and not board2.is_game_over()
    
    def test_stability(player:Player):
        board = Board()
        for i in range(int(len(board.grid)/2)):
            board.grid[i] = [player.color.value] * len(board.grid)

        board2 = Board()
        board2.grid = [[player.color.value] * Board.SIZE for _ in range(Board.SIZE)]

        return not board.is_stable_piece(Point(3, 4), Color.WHITE) and board2.is_stable_piece(Point(3, 3), player.color)

    def test_closest_corner(player:Player):
        board = Board()
        return board.get_closest_corner(Point(1, 1)) == Point(0, 0) and board.get_closest_corner(Point(4, 4)) == Point(7, 7)

    def test_diagonal_corner_placement(player:Player):
        """
        This test verifies that the player consistently prioritizes corner placement on the board.
        By placing the player's and opponent's pieces in opposite corners and introducing an additional option,
        it ensures that the player consistently chooses the corner. The loop iterates multiple times to confirm
        the player's behavior. Failure indicates inconsistency in corner placement strategy.
        """
        board = Board()
        opponent_color = Color.WHITE if player.color == Color.BLACK else Color.BLACK
        board.grid[1][1] = opponent_color.value # corners
        board.grid[2][2] = player.color.value # corners
        board.grid[5][4] = opponent_color.value # Adding other option

        for _ in range(100):
            placement_point = player.play(board)
            if placement_point != Point(0, 0):
                return False

        return True

    def test_line_corner_placement(player:Player):
        """
        This test confirms the player's preference for corner placement over forming lines.
        The player's and opponent's pieces are positioned to create a line formation along one edge of the board,
        while other options are made available. By iterating through multiple placements, the test ensures
        the player consistently chooses the corner over line formation. Failure indicates deviation from
        the expected corner placement strategy.
        """
        board = Board()
        opponent_color = Color.WHITE if player.color == Color.BLACK else Color.BLACK
        board.grid[1][0] = opponent_color.value # corners
        board.grid[2][0] = player.color.value # corners

        # Adding other options
        board.grid[5][4] = opponent_color.value 
        board.grid[2][2] = opponent_color.value 
        board.grid[3][1] = opponent_color.value 
        board.grid[3][2] = opponent_color.value 

        for _ in range(100):
            placement_point = player.play(board)
            if placement_point != Point(0, 0):
                return False
        return True

