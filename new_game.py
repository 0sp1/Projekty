import pygame

class GameBoard():
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]

    def draw_grid(self, screen, cell_size):
        for i in range(1,3):
            #horizontal lines
            x = cell_size *i
            pygame.draw.line(screen, "black", (0,x), (600, x))
            #vertical lines 
            y = x
            pygame.draw.line(screen, "black", (y, 0), (y, 600))

    def empty_cells(self):
        return [(i,j) for i in range(3) for j in range(3) if self.board[i][j] == " "]

    def draw_O(self):
        pass
    def draw_X(self):
        pass

# pygame setup
pygame.init()
WIDTH, HEIGHT = 600, 600
cell_size = 200
game = GameBoard()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("grey")

    # RENDER YOUR GAME HERE
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        col, row =  pygame.mouse.get_pos()
        col = col//cell_size
        row = row//cell_size
        if game.empty_cells(row, col):
            game.board[row][col] = "X"
            print(col, row)

    print(game.empty_cells())
    game.draw_grid(screen, cell_size)

    
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()