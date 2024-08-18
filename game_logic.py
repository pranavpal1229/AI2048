import numpy as np
import random 
grid_size = 4

class GameLogic:
    def __init__(self):
        self.grid = np.zeros((grid_size, grid_size ))       
        self.choices = [2,4]
        self.probabilities = [0.9, 0.1]

    def __str__(self):
        return str(self.grid)

    def choose_number(self):
        return random.choices(self.choices, self.probabilities)[0]


    def new_number(self, k = 1):
        open_positions = list(zip(*np.where(self.grid == 0)))
        if len(open_positions) < k:
            print("RAN OUT OF ROOM")
        original_pos = random.sample(open_positions, k)

        for pos in original_pos:
            self.grid[pos] = self.choose_number()




#------------------------------------------------------------------------------

    def move_left(self, row):
        new_row = [tile for tile in row if tile != 0] #shifts all of the number tiles to the beginning
        new_row += [0] * (grid_size - len(new_row))  
        return new_row
    
    def move_right(self, row):
        final_row = [0] * 4
        pointer = 3 #lets me work backwards when seeing the last location of non-neg
        for i in range(len(row) - 1, -1, -1):
            if row[i] != 0:
                final_row[pointer] = row[i]
                pointer -= 1
        return final_row
#------------------------------------------------------------------------------
    def combine_row_right(self, row):
        m = len(row)
        for i in range(m - 1, -1, -1):
            if row[i] != 0 and row[i - 1] == row[i]:
                row[i] *= 2
                row[i - 1] = 0
        return row
    def combine_row_left(self, row):
        m = len(row)
        for i in range(m - 1):
            if row[i] != 0 and row[i + 1] == row[i]:
                row[i] *= 2
                row[i + 1] = 0
        return row

#it is literally 2 A.M right now...if anyone is seeing this comment you
# will genuinly get a cookie if you email me at pranavpal12@gmail.com

    def make_move(self, move):
        old_board_state = self.grid.copy() #used to check if board state is different after move
        if move == "l":  # Move left
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
            self.grid = self.grid.T #transposed array and will retranspose at the end
            for row in range(grid_size):
                new_row = self.move_left(self.grid[row])
                new_row = self.combine_row_left(new_row)
                self.grid[row] = self.move_left(new_row)
            self.grid = self.grid.T


        if move == "d":
            self.grid = self.grid.T #same as above transpose function
            for row in range(grid_size):
                new_row = self.move_right(self.grid[row])
                new_row = self.combine_row_right(self.grid[row])
                self.grid[row] = self.move_right(new_row)
            self.grid = self.grid.T
        if not np.array_equal(self.grid,old_board_state):
            self.new_number()
#-----------------------------------------------------------------------------
    def play(self):
        self.new_number(k = 2)
        while True:
            print(self.grid)
            cmd = input()
            if cmd == "q":
                break
            self.make_move(cmd)





#------------------------------------------------------------------------------
if __name__ == '__main__':
    game = GameLogic()
    game.play()
