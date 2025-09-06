import pygame
import sys

CELL_SIZE = 20
WIDTH, HEIGHT = 640, 480
BG_COLOR = (30, 30, 30)
GRID_COLOR = (70, 70, 70)
ALIVE_COLOR = (255, 255, 0)

class GameBoard:
    def __init__(self, surface, cell_size):
        self.surface = surface
        self.cell_size = cell_size
        w, h = surface.get_size()

        # Compute how many rows and columns fit
        self.cols = w // cell_size
        self.rows = h // cell_size

        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(col*self.cell_size, row*self.cell_size, self.cell_size, self.cell_size)
                
                if self.board[row][col] == 1:
                    pygame.draw.rect(self.surface, ALIVE_COLOR, rect)

                # Draw grid outline
                pygame.draw.rect(self.surface, GRID_COLOR, rect, 1)

    def toggle_cell(self, x, y):
        col = x // self.cell_size
        row = y // self.cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.board[row][col] = 1 - self.board[row][col]

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("game of life")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 24)

    # Create board object
    board = GameBoard(screen, CELL_SIZE)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                board.toggle_cell(mouse_x, mouse_y)

        screen.fill(BG_COLOR)

        # Use method from GameBoard
        board.draw_grid()

        # Get mouse position
        

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
