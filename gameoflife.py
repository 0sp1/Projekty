import pygame
import sys
import random

CELL_SIZE = 20
WIDTH, HEIGHT = 1000, 800
BG_COLOR = (155, 155, 155)
GRID_COLOR = (0, 0, 0)
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

    def neighbor_cells(self, x,y):
        neighbor_count = 0
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if dx == 0  and dy == 0:
                    continue
                n_row, n_col = x + dx, y + dy
                if 0 <= n_row < self.rows and 0 <= n_col < self.cols:
                    neighbor_count += self.board[n_row][n_col]

        return neighbor_count
    
    def update(self):
        new_board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                alive_cell = self.board[row][col] == 1
                neighbor = self.neighbor_cells(row, col)

                if alive_cell:
                    if 2 > neighbor or neighbor > 3:
                        new_board[row][col] = 0
                    else:
                        new_board[row][col] = 1
                else:
                    if neighbor == 3:
                        new_board[row][col] = 1
        self.board = new_board

    def clear(self):
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        
    def randomize(self):
        self.board = [[random.randint(0,1) for _ in range(self.cols)] for _ in range(self.rows)]
        
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("game of life")
    clock = pygame.time.Clock()

    # Create board object
    board = GameBoard(screen, CELL_SIZE)
    running_simulation = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and not running_simulation:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                board.toggle_cell(mouse_x, mouse_y)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running_simulation = not running_simulation 
                elif event.key == pygame.K_c:
                    board.clear()
                elif event.key == pygame.K_r:
                    board.randomize()

        screen.fill(BG_COLOR)

        # Use method from GameBoard
        font = pygame.font.SysFont(None, 36)
        board.draw_grid()
        status_text = "Running" if running_simulation else "Paused"
        text_surface = font.render(status_text, True, (0, 0, 0))  # black text
        screen.blit(text_surface, (10, 10))
        if running_simulation:
            board.update()
                    
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()