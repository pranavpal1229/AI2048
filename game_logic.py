import numpy as np
import random 

grid_size = 4
SCORE = 0
class GameLogic:
    def __init__(self):
        self.grid = np.zeros((grid_size, grid_size), dtype=int)
        self.choices = [2, 4]
        self.probabilities = [0.9, 0.1]
        self.new_number(k=2)

    def __str__(self):
        return str(self.grid.astype(int))

    def choose_number(self):
        return int(random.choices(self.choices, self.probabilities)[0])

    def open_pos(self, grid):
        return len(list(zip(*np.where(grid == 0))))

    def new_number(self, k=1):
        open_positions = list(zip(*np.where(self.grid == 0)))
        original_pos = random.sample(open_positions, k)
        for pos in original_pos:
            self.grid[pos] = self.choose_number()

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
    def make_move(self, move):
        old_board_state = self.grid.copy()
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
        print(self.get_score())
        if not np.array_equal(self.grid, old_board_state) and self.open_pos(self.grid) != 0:
            self.new_number()
        elif self.open_pos(self.grid) == 0:
            print("RAN OUT OF ROOM")

