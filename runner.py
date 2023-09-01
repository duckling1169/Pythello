from game.board import Board
from game.enums import DiscEnum
from game.point import Point
from players.player import Player
from players.mcts_player import MCTSPlayer
from players.minimax_player import MiniMaxPlayer
from players.random_player import RandomPlayer
from players.random_learning_player import RandomLearningPlayer

import copy
from time import perf_counter


class Runner:

    def __init__(self):

        # learning_player = RandomLearningPlayer(DiscEnum.BLACK, 1000)

        # print(learning_player.custom_values)
        
        Runner.compare_players(MCTSPlayer(DiscEnum.BLACK), RandomPlayer(DiscEnum.WHITE), 10, False)


    @staticmethod
    def play_game(players, show_game=False):
        board = Board(Board.SIZE)
        if show_game:
            start = perf_counter()
            print(board)

        while not board.is_game_over():
            for player in players:
                if show_game:
                    print(f'{player}\'s turn.')

                playable_points = board.get_all_playable_points(player.color)

                if not playable_points:
                    if show_game:
                        print(f'No available spots for {player}.')
                    continue

                placement_point = player.play(board)
                while placement_point not in playable_points:
                    if show_game:
                        print(f'Invalid move by {player}.')
                    placement_point = player.play(board)

                board.can_place_disc_and_flip(placement_point, player.color)

                if show_game:
                    print(f'{player} played at {placement_point}.')
                    print(board)

        players[0].score = board.calculate_color_points(players[0].color)
        players[1].score = board.calculate_color_points(players[1].color)

        if show_game:
            print(f'Time taken: {perf_counter() - start}')

        return None if players[0].score == players[1].score else max(players, key=lambda p: p.score)

    @staticmethod
    def compare_players(player1: Player, player2: Player, games=10, show_game=False):
        winners_dict = {}

        for _ in range(games):

            winner = Runner.play_game([player1, player2], show_game)

            # Determine the category (winner or tie)
            category = 'Tie' if winner is None else type(winner).__name__

            # Extract the color if it's a player
            color = winner.color.name.title() if category != 'Tie' else None

            # Initialize and update the count in the winners_dict
            winners_dict.setdefault(category, {}).setdefault(color, 0)
            winners_dict[category][color] += 1

        print(f'\n----------\nResults from {games} games:')

        for name, data in winners_dict.items():
            for color, count in data.items():
                print(f'\t{name} as {color}: {count}/{games}')


Runner()

class Tester:

    def __init__(self):
        func_list = [func for func in dir(Tester) if callable(getattr(Tester, func)) and 'test' in func ]

        for func in func_list:
            print(f'{func}: {getattr(Tester, func)()}')

    def test_scale():
        board = Board(Board.SIZE, scale=2)
        return board.scale == 2

    def test_place_disc():
        board = Board(Board.SIZE)
        res1 = any(board.can_place_disc_and_flip(Point(3, 2), DiscEnum.BLACK))
        res2 = any(board.can_place_disc_and_flip(Point(4, 2), DiscEnum.BLACK))
        return not res1 and res2

    def test_board_copy():
        board = Board(Board.SIZE)
        board2 = copy.deepcopy(board)
        board.can_place_disc_and_flip(Point(3, 2), DiscEnum.BLACK)
        board2.can_place_disc_and_flip(Point(4, 2), DiscEnum.BLACK)
        return board != board2
    
    def test_all_playable_spots():
        board = Board(Board.SIZE)
        points = board.get_all_playable_points(DiscEnum.BLACK)
        board.can_place_disc_and_flip(points[0], DiscEnum.BLACK)
        points = board.get_all_playable_points(DiscEnum.WHITE)
        return points == [Point(2,3), Point(2,5), Point(4,5)]

    def test_is_game_over():
        board = Board(Board.SIZE)
        board2 = Board(Board.SIZE)
        board.grid = [[DiscEnum.BLACK.value] * len(board.grid) for _ in range(len(board.grid))]
        return board.is_game_over() and not board2.is_game_over()

