import numpy as np
import random 
grid_size = 4

class GameLogic:
    def __init__(self):
        self.grid = np.zeros((grid_size , grid_size))
        self.choices = [2,4]
        self.probabilities = [0.9, 0.1]

    def __str__(self):
        return str(self.grid)

    def choose_number(self):
        return random.choices(self.choices, self.probabilities)[0]


    def new_number(self, k = 1):
        open_positions = list(zip(*np.where(self.grid == 0)))
        original_pos = random.sample(open_positions, k)

        for pos in original_pos:
            self.grid[pos] = self.choose_number()

    def move_left(self, row):
        new_row = [tile for tile in row if tile != 0] #shifts all of the number tiles to the beginning
        new_row += [0] * (grid_size - len(new_row))  
        return new_row
    
    def combine_row(self, row):
        m = len(row)
        final_row = []
        for i in range(m - 1):
            if row[i] != 0 and row[i + 1] == row[i]: #if there are two adjacent numbers...combine them
                final_row.append((row[i]) * 2)
                row[i + 1] = 0 #ensures that three in a row will not combine all three
            elif row[i] != 0:
                final_row.append(row[i])
        final_row += [0] * (grid_size - len(final_row))
        return final_row

#it is literally 2 A.M right now...if anyone is seeing this comment you
# will genuinly get a cookie if you email me at pranavpal12@gmail.com

    def make_move(self, move):
        if move == "l":  # Move left
            for row in range(grid_size):
                
                new_row = self.move_left(self.grid[row])
                new_row = self.combine_row(new_row)
                self.grid[row] = self.move_left(new_row)


if __name__ == '__main__':
    game = GameLogic()
    game.new_number(8)
    print(game)
    game.make_move(move = "l")
    print(game)