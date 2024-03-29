from game.board import Board
from game.enums import Color
from game.point import Point
from players.player import Player
from players.random_player import RandomPlayer
from players.minimax_player import MiniMaxPlayer
from players.heuristics_players import HeuristicPlayer

import copy
from time import perf_counter

class HeuristicTester:

    def __init__(self, player):
        func_list = [func for func in dir(HeuristicTester) if callable(getattr(HeuristicTester, func)) and 'test' in func ]
        print(f'HeuristicTester running {len(func_list)} tests.')
        for func in func_list:
            print(f'{func}: {getattr(HeuristicTester, func)(player)}')

    def test_winner_heuristic(player:Player):
        board = Board()
        board2 = Board()
        board2.grid[2][2] = player.color.value
        board3 = Board()
        opponent_color = Color.WHITE if player.color == Color.BLACK else Color.BLACK
        board3.grid[2][2] = opponent_color.value

        print(board.winner_heuristic(player.color), board2.winner_heuristic(player.color), board3.winner_heuristic(player.color))
        return board.winner_heuristic(player.color) == 0 and board2.winner_heuristic(player.color) == -100 and board3.winner_heuristic(player.color) == 100
    
    def test_points_heuristic(player:Player):
        board = Board()
        board.grid[2][2] = player.color.value
        board2 = Board()
        opponent_color = Color.WHITE if player.color == Color.BLACK else Color.BLACK
        board2.grid = [[opponent_color.value] * len(board.grid) for _ in range(len(board.grid))]
        return board.points_heuristic(player.color) == -1 and board2.points_heuristic(player.color) == -64
    
    def test_mobility_heuristic(player:Player):
        board = Board()
        board.grid[2][3] = player.color.value
        board2 = Board()
        opponent_color = Color.WHITE if player.color == Color.BLACK else Color.BLACK
        board2.grid[2][4] = opponent_color.value
        return board.mobility_heuristic(player.color) == -2 and board2.mobility_heuristic(player.color) == 2
    
    def test_stability_heuristic(player:Player):
        board = Board()
        for i in range(int(len(board.grid)/2)):
            board.grid[i] = [player.color.value] * len(board.grid)
        board2 = Board()
        return board.stability_heuristic(player.color) == 32 and board2.stability_heuristic(player.color) == 0

    def test_square_heuristic(player:Player):
        board = Board()
        opponent_color = Color.WHITE if player.color == Color.BLACK else Color.BLACK
        board.grid[0][0] = opponent_color.value # corner - -10
        board.grid[1][0] = player.color.value # x square - 0
        board.grid[1][1] = player.color.value # c square - 0

        board.grid[3][3] = Color.EMPTY.value 
        board.grid[4][3] = Color.EMPTY.value 
        board.grid[3][4] = Color.EMPTY.value 
        board.grid[4][4] = Color.EMPTY.value 

        board2 = Board()
        opponent_color = Color.WHITE if player.color == Color.BLACK else Color.BLACK
        board2.grid[0][0] = player.color.value # corner - +10
        board.grid[1][0] = player.color.value # x square - 0
        board.grid[1][1] = player.color.value # c square - 0

        board2.grid[3][3] = Color.EMPTY.value 
        board2.grid[4][3] = Color.EMPTY.value 
        board2.grid[3][4] = Color.EMPTY.value 
        board2.grid[4][4] = Color.EMPTY.value 

        board3 = Board()
        opponent_color = Color.WHITE if player.color == Color.BLACK else Color.BLACK
        # board3.grid[0][0] = player.color.value
        board3.grid[1][0] = player.color.value # x square - -3
        board3.grid[1][1] = player.color.value # c square - -5

        board3.grid[3][3] = Color.EMPTY.value 
        board3.grid[4][3] = Color.EMPTY.value 
        board3.grid[3][4] = Color.EMPTY.value 
        board3.grid[4][4] = Color.EMPTY.value 

        return board.square_heuristic(player.color) == -10 and board2.square_heuristic(player.color) == 10 and board3.square_heuristic(player.color) == -7
    
