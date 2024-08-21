from game_logic import GameLogic
import tensorflow as tf
import numpy as np
import random
from random import randint
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LeakyReLU
from tensorflow.keras.layers import BatchNormalization, Dropout
import math
import sys
import io

# Set default encoding to utf-8 for stdout and stderr
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
class Game_2048NN:
    def __init__(self, initial_games=100, test_games= 100, goal_steps=100, lr=1e-2):
        self.initial_games = initial_games
        self.test_games = test_games
        self.goal_steps = goal_steps
        self.lr = lr
        self.vectors_and_keys = [
                ["l", 0],
                ["r", 1],
                ["u", 2],
                ["d", 3]
                ]

    def initial_population(self, num_games=100):
        population_data = []
        for _ in range(num_games):
            game = GameLogic()
            while not game.done:
                move = self.generate_random_move()
                reward = game.make_move(move)

                observations = self.generate_observations(game, move, game.done)
                observations = np.append(observations, reward[0:3])
                print(len(observations))
                rewards = np.zeros(4)
                move_index = next((i for i, v in enumerate(self.vectors_and_keys) if v[0] == move), None)
                if move_index is not None:
                    rewards[move_index] = reward[3]
                else:
                    print(f"Move {move} not found in vectors_and_keys")
                
                population_data.append((observations, rewards))
                
        # Convert the list of tuples to a NumPy array
        population_data_np = np.array(population_data, dtype=object)
        return population_data_np
    def generate_random_move(self):
        num = randint(0, 3)
        moves = ["l", "r", "u", "d"]
        return moves[num]

    def generate_observations(self, game, move, done):
        grid = np.copy(game.grid)
        grid_flattened = grid.reshape(-1)
        row_sums = np.sum(grid, axis=1)  
        col_sums = np.sum(grid, axis=0)  
        empty_count = np.sum(grid == 0) 
        
        # Features related to the move
        moves = ["l", "r", "u", "d"]
        move_index = moves.index(move) if move in moves else -1
        
        # Adding additional features
        features = np.concatenate([
            grid_flattened,
            row_sums,
            col_sums,
            [empty_count],
            [move_index],
            [1 if done else 0]
        ])
        
        return features


    def model(self):
        model = Sequential([
            tf.keras.Input(shape=(30,)),
            Dense(64, activation='relu'),
            Dense(32, activation='relu'),
            Dense(16, activation='relu'),
            Dense(4, activation='linear')
        ])

        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=self.lr),
                      loss='mean_squared_error')
        return model
    
    def train_model(self, training_data, nn_model):
        features = np.array([x[0] for x in training_data])
        rewards = np.array([x[1] for x in training_data])
        
        features = (features - np.mean(features, axis=0)) / np.std(features, axis=0)
        
        nn_model.fit(features, rewards, epochs=50, batch_size=64, validation_split=0.1)
        return nn_model


    def test_model(self, nn_model):
        total_score = 0
        total_max_tiles = []
        for i in range(self.test_games):
            print(f"NEW GAME: {i}")
            game = GameLogic()
            done = False
            while not done:
                observations = self.generate_observations(game, 'l', game.done)  # Use a placeholder move
                
                observations = np.expand_dims(observations, axis=0)
                observations = np.append(observations, np.array([[0, 0, 0]]), axis=1)

                if observations.shape != (1, 30):
                    observations = np.reshape(observations, (1, 30))
                
                predicted_rewards = nn_model.predict(observations)
                action_index = np.argmax(predicted_rewards)  

                moves = ["l", "r", "u", "d"]
                move = moves[action_index]
                copy_grid = np.copy(game.grid)
                reward = game.make_move(move)

                if np.array_equal(copy_grid, game.grid):
                    available_moves = [m for m in moves if m != move]
                    for alternative_move in available_moves:
                        copy_grid = np.copy(game.grid)
                        reward = game.make_move(alternative_move)
                        if not np.array_equal(copy_grid, game.grid):
                            break

                done = game.done
            max_tile = game.max_square(game.grid)
            total_max_tiles.append(max_tile)
            print(total_max_tiles)
            total_score += game.get_score()

        avg_score = total_score / self.test_games
        print(f"Average Score over {self.test_games} games: {avg_score}")



    def train(self):
        training_data = self.initial_population()
        nn_model = self.model()
        nn_model = self.train_model(training_data, nn_model)
        self.test_model(nn_model)

if __name__ == "__main__":
    game = Game_2048NN()
    game.train() 
