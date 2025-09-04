import pygame
import sys

# --- Settings ---
CELL_SIZE = 20
WIDTH, HEIGHT = 640, 480
BG_COLOR = (30, 30, 30)
GRID_COLOR = (70, 70, 70)
TEXT_COLOR = (200, 200, 200)


class GameBoard:
    def __init__(self, surface, cell_size):
        self.surface = surface
        self.cell_size = cell_size
        w, h = surface.get_size()

        # Compute how many rows and columns fit
        self.cols = w // cell_size
        self.rows = h // cell_size

        # Initialize the board as a 2D list (all 0s for now)
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def draw_grid(self, color):
        w, h = self.surface.get_size()
        # Vertical lines
        for x in range(0, w + 1, self.cell_size):
            pygame.draw.line(self.surface, color, (x, 0), (x, h))
        # Horizontal lines
        for y in range(0, h + 1, self.cell_size):
            pygame.draw.line(self.surface, color, (0, y), (w, y))


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

        screen.fill(BG_COLOR)

        # Use method from GameBoard
        board.draw_grid(GRID_COLOR)

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Draw text showing position
        text_surface = font.render(f"Mouse: ({mouse_x}, {mouse_y})", True, TEXT_COLOR)
        screen.blit(text_surface, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
