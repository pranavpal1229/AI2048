from game_logic import GameLogic
import tensorflow as tf
import numpy as np
import random
from random import randint

class Game_2048NN:
    def __init__(self, initial_games=100, test_games=100, goal_steps=100, lr=1e-2):
        self.initial_games = initial_games
        self.test_games = test_games
        self.goal_steps = goal_steps
        self.lr = lr
        self.vectors_and_keys = [
                ["l", 2],
                ["r", 3],
                ["u", 4],
                ["d", 5]
                ]


    def initial_population(self, num_games=100):
        population_data = []
        for _ in range(num_games):
            game = GameLogic()
            while not(game.done):
                move = self.generate_random_move()
                reward = game.make_move(move)

                observations = self.generate_observations(game, move, game.done)
        
            # Format data for training; include observation and whether the game is over
                population_data.append((observations, reward))
    
        return population_data

    def generate_random_move(self):
        num = randint(0,3)
        moves = ["l", "r", "u", "d"]
        return moves[num]

    def generate_observations(self, game, move, done):
        grid = np.copy(game.grid)
        return [grid, move, game.done]

    def model(self):
        # Define and return the neural network model
        pass

    def train_model(self, training_data, nn_model):
        # Train the neural network model
        pass

    def test_model(self, nn_model):
        # Test the neural network model
        pass

    def train(self):
        training_data = self.initial_population()
        nn_model = self.model()
        nn_model = self.train_model(training_data, nn_model)
        self.test_model(nn_model)

if __name__ == "__main__":
    game = Game_2048NN()
    training_data = game.initial_population(2)
    print(training_data)  # Or use it for your AI model





# """ 
#  """    def generate_action(self, grid, game):
#         action = randint(2,5)
#         return action, self.get_game_action(grid, action, game)

#     def get_game_action(self, grid, action, game):
#         game.grid = grid
#         if action == 2:
#             game.make_move("l")
#         elif action == 3:
#             game.make_move("u")
#         elif action == 4:
#             game.make_move("r")
#         elif action == 5:
#             game.make_move("d")
#         for pair in self.vectors_and_keys:
#             if pair[1] == action:
#                 return pair[0]

#     def generate_observation(self, grid):
#         move_left = self.can_move_left(np.copy(grid))
#         move_right = self.can_move_right(np.copy(grid))
#         move_up = self.can_move_up(np.copy(grid))
#         move_down = self.can_move_down(np.copy(grid))
#         # Return observation based on moves
#         return np.array([move_left, move_right, move_up, move_down])

#     def can_move_left(self, grid):
#         game = GameLogic()
#         game.grid = grid
#         grid_copy = np.copy(game.grid)
#         game.make_move("l")
#         if np.array_equal(grid_copy, game.grid):
#             return 0
#         return 1

#     def can_move_right(self, grid):
#         game = GameLogic()
#         game.grid = grid
#         grid_copy = np.copy(game.grid)
#         game.make_move("r")
#         if np.array_equal(grid_copy, game.grid):
#             return 0
#         return 1

#     def can_move_up(self, grid):
#         game = GameLogic()
#         game.grid = grid
#         grid_copy = np.copy(game.grid)
#         game.make_move("u")
#         if np.array_equal(grid_copy, game.grid):
#             return 0
#         return 1

#     def can_move_down(self, grid):
#         game = GameLogic()
#         game.grid = grid
#         grid_copy = np.copy(game.grid)
#         game.make_move("d")
#         if np.array_equal(grid_copy, game.grid):
#             return 0
#         return 1 """ """