from game.point import Point
from game.enums import DiscEnum
from game.board import Board
from players.player import Player
import random
import math
import copy

class MCTSPlayer(Player):

    def __init__(self, color: DiscEnum, iterations: int = 1000):
        super().__init__(color)
        self.iterations = iterations

    def mcts(self, root_node):
        for _ in range(self.iterations):
            # Selection Phase
            selected_node = self.select(root_node)

            # Expansion Phase
            if selected_node is not None:
                expanded_node = self.expand(selected_node)

                # Simulation Phase
                if expanded_node is not None:
                    result = self.simulate(expanded_node)
                else:
                    result = 0  # No valid child nodes, consider a draw
                self.backpropagate(expanded_node, result)


    def select(self, node):
        C = 1.0  # UCB1 exploration constant
        
        # Check if there are child nodes
        if not node.children:
            return node  # If there are no children, return the current node
        
        children_with_values = [(child, child.value / (child.visits + 1e-6) + C * (math.sqrt(math.log(node.visits + 1) / (child.visits + 1e-6)))) for child in node.children]
        best_child = max(children_with_values, key=lambda x: x[1])
        
        return best_child[0]  # Return the best child node

    def expand(self, node):
        legal_moves = node.state.get_all_playable_points(node.color)
        for move in legal_moves:
            new_state = copy.deepcopy(node.state)  # Copy the current game state
            new_state.can_place_disc_and_flip(move, node.color)  # Apply the move to the cloned state
            other_color = DiscEnum.BLACK if self.color == DiscEnum.WHITE else DiscEnum.WHITE 
            new_node = Node(new_state, other_color, move)  # Create a new child node
            node.children.append(new_node)
        if node.children:
            return random.choice(node.children)  # Return a randomly selected child node
        else:
            return None
    
    def simulate(self, node):
        current_state = copy.deepcopy(node.state) 
        while not current_state.is_game_over():
            legal_moves = current_state.get_all_playable_points(node.color)
            if legal_moves:
                random_move = random.choice(legal_moves)
                current_state.can_place_disc_and_flip(random_move, node.color)
                node.color = DiscEnum.WHITE if node.color == DiscEnum.BLACK else DiscEnum.BLACK
            else:
                node.color = DiscEnum.WHITE if node.color == DiscEnum.BLACK else DiscEnum.BLACK

        # Game over
        winner = current_state.get_winner(self.color)
        return winner

    def backpropagate(self, node, result):
        while node is not None:
            node.visits += 1
            node.value += result
            node = node.parent

    def select_best_move(self, root_node):
        if not root_node.children:
            return None  # No legal moves available
        else:
            best_child = max(root_node.children, key=lambda child: child.visits)
            return best_child.move

    def play(self, board: Board) -> Point:
        # Initialize the root node with the current game state
        root_node = Node(board, self.color)

        # Run MCTS for a specified number of iterations
        self.mcts(root_node)

        # Select the best move based on child node visits
        best_move = self.select_best_move(root_node)

        # Return the move associated with the best child node
        return best_move

class Node:
    def __init__(self, state, color, move=None):
        self.state = state
        self.color = color
        self.move = move
        self.children = []
        self.visits = 0
        self.value = 0
        self.parent = None

