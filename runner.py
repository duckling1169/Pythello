from game.board import Board
from game.enums import Color
from game.point import Point
from players.player import Player
from players.random_player import RandomPlayer
from players.minimax_player import MiniMaxPlayer
from players.heuristics_players import HeuristicPlayer
from players.heuristics_players import square_heuristic, mobility_heuristic, stability_heuristic, points_heuristic

import copy
from time import perf_counter

class Runner:

    def __init__(self):
        # Runner.compare_players(HeuristicPlayer(Color.WHITE, square_heuristic), RandomPlayer(Color.BLACK), 100)
        # Runner.compare_players(HeuristicPlayer(Color.WHITE, mobility_heuristic), RandomPlayer(Color.BLACK), 100)
        # Runner.compare_players(HeuristicPlayer(Color.WHITE, stability_heuristic), RandomPlayer(Color.BLACK), 100)
        # Runner.compare_players(HeuristicPlayer(Color.WHITE, points_heuristic), RandomPlayer(Color.BLACK), 100)

        # Runner.compare_players(MiniMaxPlayer(Color.WHITE, 2), RandomPlayer(Color.BLACK), 10, show_game=True) # 6secs. 9/10
        Runner.compare_players(MiniMaxPlayer(Color.WHITE, 3), RandomPlayer(Color.BLACK), 10, show_game=True) # 33secs. 9/10
        # Runner.compare_players(MiniMaxPlayer(Color.WHITE, 4), RandomPlayer(Color.BLACK), 10)

    @staticmethod
    def play_game(players:[Player, Player], show_game:bool=False):
        """
        Play a game between two players.

        Args:
            players (list): A list of two Player objects.
            show_game (bool, optional): Whether to display the game board during play (default is False).

        Returns:
            Player: The winner of the game or None if it's a tie.
        """
        board = Board()
        
        if show_game:
            start = perf_counter()
            print(board)

        while not board.is_game_over():
            for player in players:
                play_start = perf_counter()
                
                if show_game:
                    print(f'{player}\'s turn.')

                playable_points = board.get_legal_moves(player.color)

                if not playable_points:
                    if show_game:
                        print(f'No available spots for {player}.')
                    continue

                placement_point = player.play(board)

                while placement_point not in playable_points:
                    if show_game:
                        print(f'Invalid move by {player}.')
                    placement_point = player.play(board)

                board.place_and_flip_discs(placement_point, player.color)

                if show_game:
                    print(f'{player} played at {placement_point} ({round(perf_counter() - play_start, 2)} secs).')
                    print(board)

        players[0].score = board.get_points_for_color(players[0].color)
        players[1].score = board.get_points_for_color(players[1].color)

        winner = None if players[0].score == players[1].score else max(players, key=lambda p: p.score)

        if show_game:
            print(f'Result is {winner}. Time taken: {round(perf_counter() - start)} secs.')

        return winner

    @staticmethod
    def compare_players(player1:Player, player2:Player, games:int = 10, show_game:bool = False, break_at_loss:bool = False):
        """
        Compare two players in a series of games and report the results.

        Args:
            player1 (Player): The class representing the first player.
            player2 (Player): The class representing the second player.
            games (int, optional): The number of games to play (default is 10).
            show_game (bool, optional): Whether to display the game during play (default is False).
        """
        # Get the start time
        start_time = perf_counter()

        # Initialize a dictionary to store the results
        winners_dict = {}

        # Play the specified number of games
        for _ in range(games):
            # Play a game between player1 and player2
            winner = Runner.play_game([player1, player2], show_game)

            if break_at_loss and winner != player1:
                break

            # Determine the category of the result (Win, Tie, or Loss)
            category = 'Tie' if winner is None else type(winner).__name__

            # Extract the color of the winner if applicable
            color = winner.color.name.title() if category != 'Tie' else None

            # Initialize and update the count in the winners_dict
            winners_dict.setdefault(category, {}).setdefault(color, 0)
            winners_dict[category][color] += 1

        # Print the results
        s = f'Results from {games} games in {round(perf_counter() - start_time, 2)} secs:'
        print('-'*len(s) + f'\n{s}')

        for name, data in winners_dict.items():
            for color, count in data.items():
                print(f'\t{name} as {color}: {count}/{games}')

class Tester:

    def __init__(self, player):
        func_list = [func for func in dir(Tester) if callable(getattr(Tester, func)) and 'test' in func ]

        for func in func_list:
            print(f'{func}: {getattr(Tester, func)(player)}')

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
    
    def test_diagonal_corner_placement(player:Player):
        board = Board()
        opponent_color = Color.WHITE if player.color == Color.BLACK else Color.BLACK
        board.grid[1][1] = opponent_color.value # corners
        board.grid[2][2] = player.color.value # corners
        # Adding other option
        board.grid[5][4] = opponent_color.value 

        for _ in range(100):
            placement_point = player.play(board)
            if placement_point != Point(0, 0):
                return False

        return True

    def test_line_corner_placement(player:Player):
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

    def test_square_heuristic(player:Player):
        board = Board()
        opponent_color = Color.WHITE if player.color == Color.BLACK else Color.BLACK
        board.grid[0][0] = opponent_color.value # corner - 10
        board.grid[1][0] = player.color.value # x square - 2
        board.grid[1][1] = player.color.value # c square - 5

        board.grid[3][3] = Color.EMPTY.value 
        board.grid[4][3] = Color.EMPTY.value 
        board.grid[3][4] = Color.EMPTY.value 
        board.grid[4][4] = Color.EMPTY.value 

        board2 = Board()
        opponent_color = Color.WHITE if player.color == Color.BLACK else Color.BLACK
        board2.grid[0][0] = player.color.value # corner + 1
        board2.grid[1][0] = player.color.value # x square + 1
        board2.grid[1][1] = player.color.value # c square + 1

        board2.grid[3][3] = Color.EMPTY.value 
        board2.grid[4][3] = Color.EMPTY.value 
        board2.grid[3][4] = Color.EMPTY.value 
        board2.grid[4][4] = Color.EMPTY.value 

        return board.square_heuristic(player.color) == -17 and board2.square_heuristic(player.color) == 3
    
    def test_find_closest_corner(player:Player):
        board = Board()
        return Point(0,0) == board.get_closest_corner(Point(2,2))

    def test_stability(player:Player):
        board = Board()
        board2 = Board()
        board2.grid = [[player.color.value] * Board.SIZE for _ in range(Board.SIZE)]
        return not board.is_stable_piece(Point(3, 3), Color.WHITE) and board2.is_stable_piece(Point(3, 3), player.color)

    def test_closest_corner(player:Player):
        board = Board()
        return board.get_closest_corner(Point(1,1)) == Point(0,0) and board.get_closest_corner(Point(4,4)) == Point(7,7)


if __name__ == "__main__":
    Runner()
    # Tester(RandomPlayer(Color.WHITE))
