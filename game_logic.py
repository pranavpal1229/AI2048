import numpy as np
import random 
import collections
import math 
grid_size = 4
SCORE = 0
class GameLogic:
    def __init__(self):
        self.grid = np.zeros((grid_size, grid_size), dtype=int)
        self.choices = [2, 4]
        self.probabilities = [0.9, 0.1]
        self.new_number(k=2)
        self.done = False
        self.trial = 'hi'

    def __str__(self):
        return str(self.grid.astype(int))

    def choose_number(self):
        return int(random.choices(self.choices, self.probabilities)[0])
    def max_square(self, grid):
        copy_grid = np.copy(grid)
        copy_grid = copy_grid.reshape(-1)
        return np.max(copy_grid)
    def open_pos(self, grid):
        return len(list(zip(*np.where(grid == 0))))

    def all_dif(self, grid):
        for row in grid:
            for i in range(len(row) - 2):
                if row[i] == row[i + 1]:
                    return False
        copy_grid = np.copy(grid)
        copy_grid = copy_grid.T
        for col in copy_grid:
            for i in range(len(col) - 2):
                if col[i] == col[i + 1]:
                    return False
        return True

    def open_positions(self, grid):
        return list(zip(*np.where(grid == 0)))

    def new_number(self, k=1):
        open_positions = list(zip(*np.where(self.grid == 0)))
        original_pos = random.sample(open_positions, k)
        for pos in original_pos:
            self.grid[pos] = self.choose_number()
    
    def reset(self):
        global SCORE
        self.grid = np.zeros((grid_size, grid_size), dtype=int)
        SCORE = 0
        self.new_number(k=2)
        return self.generate_observations()
    # Move functions and combination functions
    def move_left(self, row):
        new_row = [tile for tile in row if tile != 0]
        new_row += [0] * (grid_size - len(new_row))  
        return new_row
    
    def move_right(self, row):
        final_row = [0] * 4
        pointer = 3
        for i in range(len(row) - 1, -1, -1):
            if row[i] != 0:
                final_row[pointer] = row[i]
                pointer -= 1
        return final_row

    def combine_row_right(self, row):
        global SCORE
        m = len(row)
        for i in range(m - 1, -1, -1):
            if row[i] != 0 and row[i - 1] == row[i]:
                row[i] *= 2
                SCORE += row[i]
                row[i - 1] = 0
        return row
    def generate_observations(self):
        return [
             self.grid.copy(),
            self.get_score(),
            self.done
        ]
    def combine_row_left(self, row):
        global SCORE
        m = len(row)
        for i in range(m - 1):
            if row[i] != 0 and row[i + 1] == row[i]:
                row[i] *= 2
                SCORE += row[i]
                row[i + 1] = 0
        return row
    def get_score(self):
        return SCORE

    def reward_calc(self, old_max, new_max, old_open, new_open, old_score, new_score, done):
        reward = 0
        max_diff = new_max - old_max
        if new_max > old_max:
            reward += 100
        if len(new_open) < len(old_open):
            reward += 25
            open_diff = len(new_open) - len(old_open)
        else:
            reward -= 50
            open_diff = len(new_open) - len(old_open)
        if new_score > old_score:
            reward += 2
            score_diff = new_score - old_score
        else:
            reward -= 15
            score_diff = new_score - old_score
        if done:
            reward -= 1000
        return [max_diff, open_diff, score_diff, reward]
    def make_move(self, move):
        old_board_state = self.grid.copy()
        old_score = SCORE
        old_max = self.max_square(self.grid)
        old_open = self.open_positions(self.grid)
        if move == "l": 
            for row in range(grid_size):
                new_row = self.move_left(self.grid[row])
                new_row = self.combine_row_left(new_row)
                self.grid[row] = self.move_left(new_row)
        if move == "r":
            for row in range(grid_size):
                new_row = self.move_right(self.grid[row])
                new_row = self.combine_row_right(new_row)
                self.grid[row] = self.move_right(new_row)

        if move == "u":
            self.grid = self.grid.T
            for row in range(grid_size):
                new_row = self.move_left(self.grid[row])
                new_row = self.combine_row_left(new_row)
                self.grid[row] = self.move_left(new_row)
            self.grid = self.grid.T

        if move == "d":
            self.grid = self.grid.T
            for row in range(grid_size):
                new_row = self.move_right(self.grid[row])
                new_row = self.combine_row_right(new_row)
                self.grid[row] = self.move_right(new_row)
            self.grid = self.grid.T
        if not np.array_equal(self.grid, old_board_state) and self.open_pos(self.grid) != 0:
            new_max = self.max_square(self.grid)
            new_open = self.open_positions(self.grid)
            self.new_number()
            return self.reward_calc(old_max, new_max, old_open, new_open, old_score, SCORE, False)
        elif self.open_pos(self.grid) == 0 and self.all_dif(self.grid):
            new_max = self.max_square(self.grid)
            new_open = self.open_positions(self.grid)           
            self.done = True
            return self.reward_calc(old_max, new_max, old_open, new_open, old_score, SCORE, True)
        else:
            new_max = self.max_square(self.grid)
            new_open = self.open_positions(self.grid) 
            return self.reward_calc(old_max, new_max, old_open, new_open, old_score, SCORE, False)