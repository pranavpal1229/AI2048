import pygame
import math
from game_logic import GameLogic, SCORE
import time
pygame.init()

FPS = 20
WIDTH, HEIGHT = 650, 650
ROWS, COLS = (4, 4)
RECT_HEIGHT = HEIGHT / COLS
RECT_WIDTH = HEIGHT / COLS

OUTLINE_COLOR = (187, 173, 160)
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205, 192, 180)
FONT_COLOR = (119, 110, 101)

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT + 100))
SCREEN = pygame.Surface((WIDTH, HEIGHT + 100), pygame.SRCALPHA)
pygame.display.set_caption("2048")
FONT = pygame.font.SysFont("comicsans", 60, bold=True)
FONT2 = pygame.font.SysFont("comicsans", 30, bold=True)

MOVE_VEL = 20

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
        pygame.draw.rect(window, (color), (self.x + 5, self.y + 5, RECT_WIDTH - 10, RECT_HEIGHT - 10))

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

    for row in range(1, COLS):
        x = row * RECT_HEIGHT
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
    """
    Draw text on a Pygame window.

    Parameters:
    - text: The string of text to be drawn.
    - font: The Pygame font object to be used for rendering the text.
    - color: A tuple representing the RGB color of the text.
    - x: The x-coordinate for the text's position.
    - y: The y-coordinate for the text's position.
    - center: If True, the text will be centered on the given (x, y) coordinates.
    """
    text_surface = font.render(text, True, color)
    if center:
        x = x - text_surface.get_width() // 2
        y = y - text_surface.get_height() // 2
    WINDOW.blit(text_surface, (x, y))

def main(window):
    clock = pygame.time.Clock()
    run = True
    last_score = board.get_score()

    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                move_made = False
                if event.key == pygame.K_LEFT:
                    move_made = board.make_move("l")
                elif event.key == pygame.K_RIGHT:
                    move_made = board.make_move("r")
                elif event.key == pygame.K_UP:
                    move_made = board.make_move("u")
                elif event.key == pygame.K_DOWN:
                    move_made = board.make_move("d")
                elif event.key == pygame.K_1:
                    move_made = board.reset()
                if move_made == False:
                    print(board.get_score())
                    pygame.display.update()  # Ensure the score is displayed before delay
                    time.sleep(5)  # Wait for 5 seconds
                    board.reset()
        
        # Draw the game board
        draw_board(window, board.grid)

        # Check if the score has changed
        current_score = board.get_score()
            # Clear the score area
        pygame.draw.rect(window, BACKGROUND_COLOR, (0, HEIGHT, WIDTH, 100))
        
        # Draw the updated score
        draw_text(f"Score: {current_score}", FONT2, (0,0,0), WIDTH // 2, HEIGHT + 50, center=True)
        
        # Update the display only for the score area
        pygame.display.update((0, HEIGHT, WIDTH, 100))


        # Update the display for the game area
        pygame.display.update((0, 0, WIDTH, HEIGHT))

    pygame.quit()

if __name__ == "__main__":
    main(WINDOW)