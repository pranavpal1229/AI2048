import pygame
import math
from game_logic import GameLogic
import time
from agent import Game_2048NN
import numpy as np
# Initialize AI
ai = Game_2048NN()
nn_model = ai.model()  # Initialize your model
# Optionally, load pre-trained weights if available
# nn_model.load_weights('path_to_weights.h5')

pygame.init()

FPS = 1  # Slow down the FPS to visualize AI moves more clearly
WIDTH, HEIGHT = 650, 650
ROWS, COLS = (4, 4)
RECT_HEIGHT = HEIGHT / COLS
RECT_WIDTH = WIDTH / ROWS

OUTLINE_COLOR = (187, 173, 160)
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205, 192, 180)
FONT_COLOR = (119, 110, 101)

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT + 100))
pygame.display.set_caption("2048 AI Visualization")
FONT = pygame.font.SysFont("comicsans", 60, bold=True)
FONT2 = pygame.font.SysFont("comicsans", 30, bold=True)

board = GameLogic()

class Tile:
    COLORS = [
        (237, 229, 218),
        (238, 225, 201),
        (243, 178, 122),
        (246, 150, 101),
        (247, 124, 95),
        (247, 95, 59),
        (237, 208, 115),
        (237, 204, 99),
        (236, 202, 80),
    ]
    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * RECT_WIDTH
        self.y = row * RECT_HEIGHT

    def get_color(self):
        color_index = int(math.log2(self.value)) - 1
        color = self.COLORS[color_index]
        return color

    def draw(self, window):
        color = self.get_color()
        pygame.draw.rect(window, color, (self.x + 5, self.y + 5, RECT_WIDTH - 10, RECT_HEIGHT - 10))
        text = FONT.render(str(self.value), 1, FONT_COLOR)
        window.blit(
            text,
            (
                self.x + (RECT_WIDTH / 2 - text.get_width() / 2),
                self.y + (RECT_HEIGHT / 2 - text.get_height() / 2),
            ),
        )

def draw_grid(window):
    for row in range(1, ROWS):
        y = row * RECT_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)
    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)

    for col in range(1, COLS):
        x = col * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)
    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)

def draw_board(window, grid):
    window.fill(BACKGROUND_COLOR)
    draw_grid(window)
    for row in range(ROWS):
        for col in range(COLS):
            value = grid[row][col]
            if value != 0:
                tile = Tile(value, row, col)
                tile.draw(window)
    pygame.display.update()

def draw_text(text, font, color, x, y, center=False):
    text_surface = font.render(text, True, color)
    if center:
        x -= text_surface.get_width() // 2
        y -= text_surface.get_height() // 2
    WINDOW.blit(text_surface, (x, y))

def main(window):
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        observations = ai.generate_observations(board, 'l', board.done)  # Dummy move, will be replaced
        
        if observations.ndim == 1:
            observations = np.expand_dims(observations, axis=0)
        
        additional_features = np.array([[0, 0, 0]])
        
        additional_features = additional_features.reshape(1, -1)

        observations = np.concatenate((observations, additional_features), axis=1)

        # Ensure the shape is correct
        print("Observations shape after concatenation:", observations.shape)

        # Predict rewards using the model
        predicted_rewards = nn_model.predict(observations)
        move_index = np.argmax(predicted_rewards)
        moves = ["l", "r", "u", "d"]
        move = moves[move_index]
        predicted_rewards[0][move_index] = -1000
        move_index2 = np.argmax(predicted_rewards)
        move2 = moves[move_index2]
        predicted_rewards[0][move_index2] = -1000
        move_index3 = np.argmax(predicted_rewards)
        move3 = moves[move_index3]
        predicted_rewards[0][move_index3] = -1000
        move_index4 = np.argmax(predicted_rewards)
        move4 = moves[move_index]

        # Make the move
        copy_grid = np.copy(board.grid)
        move_made = board.make_move(move)
        if np.array_equal(copy_grid, board.grid):
            board.make_move(move2)
            if np.array_equal(copy_grid, board.grid):
                board.make_move(move3)
                if np.array_equal(copy_grid, board.grid):
                    board.make_move(move4)

        if not move_made:
            print(board.get_score())
            pygame.display.update()
            time.sleep(5)
            board.reset()

        draw_board(window, board.grid)

        current_score = board.get_score()
        pygame.draw.rect(window, BACKGROUND_COLOR, (0, HEIGHT, WIDTH, 100))
        draw_text(f"Score: {current_score}", FONT2, (0, 0, 0), WIDTH // 2, HEIGHT + 50, center=True)
        pygame.display.update((0, HEIGHT, WIDTH, 100))
        pygame.display.update((0, 0, WIDTH, HEIGHT))

    pygame.quit()

if __name__ == "__main__":
    main(WINDOW)
