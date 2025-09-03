import pygame
import sys

# --- Settings ---
CELL_SIZE = 20
WIDTH, HEIGHT = 640, 480
BG_COLOR = (30, 30, 30)
GRID_COLOR = (70, 70, 70)
TEXT_COLOR = (200, 200, 200)

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
    clock = pygame.time.Clock()

    # Font for text
    font = pygame.font.SysFont(None, 24)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG_COLOR)
        draw_grid(screen, CELL_SIZE, GRID_COLOR)

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
