from game.board import Board
from game.enums import Color
from players.player import Player
from players.random_player import RandomPlayer
from players.minimax_player import MiniMaxPlayer
from players.heuristics_players import HeuristicPlayer
from players.mcts_player import MCTSPlayer

from tests.board_tester import BoardTester
from tests.heuristic_tester import HeuristicTester
from typing import List, Type, Union
from collections import defaultdict


from time import perf_counter

class Runner:

    @staticmethod
    def play_game(players: Union[Player, Player], show_game:bool = False):
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
        start_time = perf_counter()
        winners_dict = defaultdict(int)

        for _ in range(games):
            winner = Runner.play_game([player1, player2], show_game)
            if break_at_loss and winner != player1: break
            winners_dict[winner] += 1

        s = f'Results from {games} games in {round(perf_counter() - start_time, 2)} secs:'
        print('-'*len(s) + f'\n{s}')

        for player, count in winners_dict.items():
            player_name = 'Tie' if player is None else type(player).__name__
            heuristic_names = f' ({player.heuristic_names})' if hasattr(player, 'heuristic_names') else ''
            print(f'\t{player_name}{heuristic_names}: {count}/{games}')

        return True

if __name__ == "__main__":

    minimax_p1 = MiniMaxPlayer(Color.WHITE, ['square_heuristic'], max_depth=2)
    minimax_p2 = MiniMaxPlayer(Color.WHITE, ['square_heuristic', 'mobility_heuristic'], max_depth=2)

    # player3 = MiniMaxPlayer(Color.WHITE, ['square_heuristic', 'mobility_heuristic', 'points_heuristic'], max_depth=1)
    # player4 = MiniMaxPlayer(Color.WHITE, ['square_heuristic', 'mobility_heuristic', 'points_heuristic', 'stability_heuristic'], max_depth=1)

    mcts_player = MCTSPlayer(Color.BLACK, 250)

    Runner.compare_players(mcts_player, minimax_p2, 1, show_game=True)

    # Runner.compare_players(player1, player3, 20)
    # Runner.compare_players(player1, player4, 20)
    # player2.color = Color.BLACK
    # Runner.compare_players(player2, player3, 20)
    # Runner.compare_players(player2, player4, 20)
    # player3.color = Color.BLACK
    # Runner.compare_players(player3, player4, 20)

    # Runner.play_all_heuristics(10)
    # BoardTester(RandomPlayer(Color.WHITE))
    # HeuristicTester(RandomPlayer(Color.WHITE))
