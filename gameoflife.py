import pygame
import sys

CELL_SIZE = 20         
WIDTH, HEIGHT = 640, 480  
BG_COLOR = (30, 30, 30)
GRID_COLOR = (70, 70, 70)

def draw_grid(surface, cell_size, color):
    w, h = surface.get_size()
    # Vertical lines
    for x in range(0, w + 1, cell_size):
        pygame.draw.line(surface, color, (x, 0), (x, h))
    # Horizontal lines
    for y in range(0, h + 1, cell_size):
        pygame.draw.line(surface, color, (0, y), (w, y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("20x20 Grid (Pygame)")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG_COLOR)
        draw_grid(screen, CELL_SIZE, GRID_COLOR)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
