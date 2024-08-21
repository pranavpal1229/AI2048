from game_logic import GameLogic
import tensorflow as tf
import numpy as np
import random
from random import randint
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LeakyReLU
import sys
import io

# Set default encoding to utf-8 for stdout and stderr
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
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
            while not game.done:
                move = self.generate_random_move()
                reward = game.make_move(move)

                observations = self.generate_observations(game, move, game.done)
                observations = np.append(observations, reward[0:3])
                assert(len(observations) == 21)
                # Format rewards as a vector with zeroes except for the action taken
                rewards = np.zeros(4)
                # Find index for the action based on the move
                move_index = next((i for i, v in enumerate(self.vectors_and_keys) if v[0] == move), None)
                if move_index is not None:
                    rewards[move_index] = reward[3]
                else:
                    print(f"Move {move} not found in vectors_and_keys")
                
                # Add the observation and reward to the training data
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
        moves = ["l", "r", "u", "d"]
        ans = 0
        done_num = 0
        if done:
            done_num = 1
        for i, num in enumerate(moves):
            if num == move:
                ans = i
                break
        grid = grid.reshape(-1)  # Flatten the grid
        grid = np.append(grid, [ans, done_num])

        
        return grid  # Return as a flat NumPy array

    def model(self):
        # Define and return the neural network model
        model = Sequential([
            tf.keras.Input(shape=(21,)),  # Input shape should match the feature size
            Dense(15, activation= 'relu'),
            Dense(5, activation= 'relu'),
            Dense(4, activation='linear')  # Assuming 4 possible actions
        ])
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=self.lr),
                      loss='mean_squared_error')
        return model

    def train_model(self, training_data, nn_model):
        features = np.array([x[0] for x in training_data])
        rewards = np.array([x[1] for x in training_data])

        # Ensure the shapes are correct
        print(f"Features shape: {features.shape}")
        print(f"Rewards shape: {rewards.shape}")

        nn_model.fit(features, rewards, epochs=10, batch_size=32)
        return nn_model

    def test_model(self, nn_model):
        total_score = 0
        for _ in range(self.test_games):
            game = GameLogic()
            done = False
            while not done:
                observations = self.generate_observations(game, '', game.done)
                observations = np.append(observations, [0,0,0])
                observations = np.array([observations])  # Add batch dimension
                print(f"Observations shape: {observations.shape}")  # Debug print
                predicted_rewards = nn_model.predict(observations)
                action_index = np.argmax(predicted_rewards)  # Choose action with the highest predicted reward
                move = self.vectors_and_keys[action_index][0]
                
                reward = game.make_move(move)
                done = game.done

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