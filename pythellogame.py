from game.board import Board
from game.enums import DiscEnum
from game.point import Point
from players.player import Player
from players.random_player import RandomPlayer
from players.aiplayer import AIPlayer

class Pythello:

    def __init__(self, scale:int=1, players:[Player]=[AIPlayer(DiscEnum.WHITE), RandomPlayer(DiscEnum.BLACK)]):
        self.board = Board(Board.SIZE, scale)
        self.players = players

    def place_disc(self, point:Point, color:DiscEnum) -> bool:
        return self.board.can_place_disc_and_flip(point, color)
    
    def is_game_over(self) -> bool:
        black_points = self.board.get_all_playable_points(DiscEnum.BLACK)
        white_points = self.board.get_all_playable_points(DiscEnum.WHITE)
        return not any(black_points) and not any(white_points)
    
    def play(self) -> str:
        while not self.is_game_over():
            for player in self.players:
                print(self.board)
                print(f'{player.color.name.title()}\'s turn. ({player.color.value})')

                playable_points = self.board.get_all_playable_points(player.color)

                if not playable_points:
                    print(f'No available spots for {player.color.name.title()}.')
                    continue

                placed = False
                while not placed:
                    placement_point = player.play(self.board)
                    print(f'{player.color.name.title()} played at {placement_point}.')
                    if placement_point in playable_points:
                        placed = self.board.can_place_disc_and_flip(placement_point, player.color)
                
                # Calculate player points while the game is still ongoing, if needed
                player.points = self.board.calculate_player_points(player)

        return f'The winner is {self.players[0].color.name.title() if self.players[0].score > self.players[1].score else self.players[1].color.name.title()}'

    def __str__(self):
        return self.board.__str__()
