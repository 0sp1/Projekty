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
        positions = {(0,0) : (100, 100), (0,1): (300, 100), (0,2): (500, 100),
                     (1,0) : (100, 300), (1,1): (300, 300), (1,2): (500, 300),
                     (2,0) : (100, 500), (2,1): (300, 500), (2,2): (500, 500)
                     }
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

player_symbol = "X" 
computer_symbol = "O"
turn = player_symbol

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("grey")

    # RENDER YOUR GAME HERE
    game.draw_grid(screen, cell_size)
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        col, row =  pygame.mouse.get_pos()
        col = col//cell_size
        row = row//cell_size
        if game.empty_cells(row, col):
            game.board[row][col] = "X"
            print(col, row)
    
    
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()

#