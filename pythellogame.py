from game.board import Board
from game.enums import DiscEnum
from game.point import Point

class Pythello:

    def __init__(self, auto:bool=True, scale:int=1):
        self.board = Board(Board.SIZE, scale)
        self.players = []

    def place_disc(self, point:Point, color:DiscEnum) -> bool:
        return self.board.can_place_disc_and_flip(point, color)
    
    def is_game_over(self) -> bool:
        black_points = self.board.get_all_playable_points(DiscEnum.BLACK)
        white_points = self.board.get_all_playable_points(DiscEnum.WHITE)
        return not any(black_points) and not any(white_points)
    
    def play(self) -> (int, int):
        while not self.is_game_over():
            for player in self.players:
                playable_points = self.board.get_all_playable_points(player.color)

                if not playable_points:
                    print(f'No available spots for {player.color.value}.')
                    continue

                placed = False
                while not placed:
                    placement_point = player.play(self.board)
                    if placement_point in playable_points:
                        placed = self.board.can_place_disc_and_flip(placement_point, player.color)
                
                # Calculate player points while the game is still ongoing, if needed
                self.calculate_player_points(player)

        # Calculate player points after the game is over
        player1_points = self.calculate_player_points(player[0])
        player2_points = self.calculate_player_points(player[1])

        return player1_points, player2_points
    
    def calculate_player_points(self, player):
        return sum(row.count(player.color.value) for row in self.board.grid)


        # while not self.is_game_over():
        #     for player in self.players:
        #         if not self.board.get_all_playable_points(player.color):
        #             print('No available spots.')
        #             continue

        #         placed = False
        #         while not placed:
        #             placement_point = player.play(self.board)
        #             placed = self.board.can_place_disc_and_flip(placement_point, player.color)
            
        # player1_points = 0
        # player2_points = 0
        # for x in range(len(self.board.grid)):
        #     for y in range(len(self.board.grid[0])):
        #         if self.board.grid[y][x] == self.players[0]:
        #             player1_points += 1
        #         if self.board.grid[y][x] == self.players[1]:
        #             player2_points += 1
        
        # return player1_points, player2_points

    def __str__(self):
        return self.board.__str__()
