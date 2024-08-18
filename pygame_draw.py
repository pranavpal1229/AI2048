import pygame
import math
from game_logic import GameLogic

pygame.init()

FPS = 60
WIDTH, HEIGHT = 800, 800
ROWS, COLS = (4, 4)
RECT_HEIGHT = HEIGHT / COLS
RECT_WIDTH = HEIGHT / COLS

OUTLINE_COLOR = (187, 173, 160)
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205, 192, 180)
FONT_COLOR = (119, 110, 101)

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")
FONT = pygame.font.SysFont("comicsans", 60, bold=True)
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



def main(window):
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    board.make_move("l")
                elif event.key == pygame.K_RIGHT:
                    board.make_move("r")
                elif event.key == pygame.K_UP:
                    board.make_move("u")
                elif event.key == pygame.K_DOWN:
                    board.make_move("d")

        draw_board(window, board.grid)
    
    pygame.quit()

if __name__ == "__main__":
    main(WINDOW)