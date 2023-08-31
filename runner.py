from pythellogame import Pythello
from game.enums import DiscEnum
from game.point import Point
import copy

class Runner:

    def __init__(self):

        gb = Pythello()
        # gb.setup_game()
        # while True:
        #     for player in gb.players:
        #         player.play()

class Tester:

    def __init__(self):
        func_list = [func for func in dir(Tester) if callable(getattr(Tester, func)) and 'test' in func ]

        for func in func_list:
            print(f'{func}: {getattr(Tester, func)()}')

    def test_scale():
        game1 = Pythello(scale=2)
        # print(game1)
        return game1.board.scale == 2

    def test_place_disc():
        game1 = Pythello()
        res1 = game1.place_disc(Point(3, 2), DiscEnum.BLACK)
        res2 = game1.place_disc(Point(4, 2), DiscEnum.BLACK)
        return not res1 and res2

    def test_board_copy():
        game1 = Pythello()
        game2 = copy.deepcopy(game1)
        game1.place_disc(Point(1, 1), DiscEnum.BLACK)
        game2.place_disc(Point(6, 6), DiscEnum.BLACK)
        return game1 != game2
    
    def test_all_playable_spots():
        game1 = Pythello()
        points = game1.board.get_all_playable_points(DiscEnum.BLACK)
        game1.place_disc(points[0], DiscEnum.BLACK)
        points = game1.board.get_all_playable_points(DiscEnum.WHITE)
        return points == [Point(2,3), Point(2,5), Point(4,5)]

    def test_is_game_over():
        game1 = Pythello()
        game2 = Pythello()
        game2.board.grid = [[DiscEnum.BLACK.value] * len(game2.board.grid) for _ in range(len(game2.board.grid))]
        return not game1.is_game_over() and game2.is_game_over()


tester = Tester()
