from game.board import Board
from game.enums import DiscEnum
from game.point import Point
from players.player import Player

from time import perf_counter

class Pythello:

    def __init__(self, scale:int=1, players:[Player]=[]):
        self.board = Board(Board.SIZE, scale)
        self.players = players
        self.start = perf_counter()

    def place_disc(self, point:Point, color:DiscEnum) -> bool:
        return any(self.board.can_place_disc_and_flip(point, color))
    
    def is_game_over(self) -> bool:
        return self.board.is_game_over()
    
    def play(self, show_game:bool = True):
        if show_game:
            print(self.board)

        while not self.is_game_over():
            for player in self.players:
                if show_game:
                    print(f'{player.color.name.title()}\'s turn. ({player.color.value})')

                playable_points = self.board.get_all_playable_points(player.color)

                if not playable_points:
                    if show_game:
                        print(f'No available spots for {player.color.name.title()}.')
                    continue

                placed = False
                while not placed:
                    placement_point = player.play(self.board)
                    if placement_point in playable_points:
                        placed = self.place_disc(placement_point, player.color)
                
                self.players[0].score = self.board.calculate_color_points(self.players[0].color)
                self.players[1].score = self.board.calculate_color_points(self.players[1].color)
                if show_game:
                    print(f'{player.color.name.title()} played at {placement_point}.')
                    print(self.board)
    
    def get_winner(self) -> Player:
        winner = None
        if self.players[0].score == self.players[1].score:
            print('Tie game!')
        
        winner = self.players[0] if self.players[0].score > self.players[1].score else self.players[1]

        print(f'The winner is {winner.color.name.title()} ({winner.color.value}) with {winner.score} points.')
        print(f'Time taken: {round(perf_counter() - self.start, 2)} secs.')

        return winner

    def __str__(self):
        return self.board.__str__()
