from game.board import Board
from game.enums import Color
from players.player import Player
from players.random_player import RandomPlayer
from players.minimax_player import MiniMaxPlayer
from players.heuristics_players import HeuristicPlayer

from tests.board_tester import BoardTester
from tests.heuristic_tester import HeuristicTester
from typing import List, Type, Union

from time import perf_counter

class Runner:

    def __init__(self):
        # Runner.compare_players(HeuristicPlayer(Color.WHITE), RandomPlayer(Color.BLACK), 100, show_game=True, break_at_loss=True)
        Runner.compare_players(Player(Color.WHITE), MiniMaxPlayer(Color.BLACK, ['square_heuristic', 'mobility_heuristic', 'points_heuristic', 'stability_heuristic'], max_depth=3), 1, show_game=True, break_at_loss=True)

        # Runner.play_all_heuristics(HeuristicPlayer, 100)
        # Runner.play_all_heuristics(MiniMaxPlayer, 1)
        # Runner.compare_players(MiniMaxPlayer(Color.WHITE, 4), RandomPlayer(Color.BLACK), 10)

    @staticmethod
    def play_game(players: Union[Player, Player], show_game:bool=False):
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

            if break_at_loss and winner != player1: break

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

        # Sort winners_dict for printing
        sorted_dict = dict(sorted(winners_dict.items()))
        for category, data in sorted_dict.items():
            sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))
            for color, count in sorted_data.items():
                print(f'\t{category} as {color}: {count}/{games}')

if __name__ == "__main__":
    Runner()
    # Runner.play_all_heuristics(10)
    # BoardTester(RandomPlayer(Color.WHITE))
    # HeuristicTester(RandomPlayer(Color.WHITE))
