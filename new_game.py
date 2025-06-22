import pygame, random

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

    def O_draw(self, screen, row, col, cell_size):
        position_x = col*cell_size
        position_y = row*cell_size
        pygame.draw.circle(screen, "black", (position_x+100, position_y+100), 80 , 4)
    
    def X_draw(self, screen, row, col, cell_size):
        position_x = col* cell_size
        position_y = row * cell_size
        
        pygame.draw.line(screen, "black", (position_x+20, position_y+20), (position_x + cell_size - 20, position_y + cell_size - 20), width=5)

        pygame.draw.line(screen, "black", (position_x + cell_size - 20, position_y + 20), (position_x + 20, position_y + cell_size - 20),width=5)

    def win_conditions(self, symbol):
        for i in range(3):
            if all(self.board[i][j] == symbol for j in range(3)) or all(self.board[j][i] == symbol for j in range(3)):
                return True

        if all(self.board[i][i] == symbol for i in range(3)) or all(self.board[i][2-i] == symbol for i in range(3)):
            return True
        return False

def player_move(game, cell_size):
            col, row =  pygame.mouse.get_pos()
            col = col//cell_size
            row = row//cell_size
            if (row, col) in game.empty_cells():
                game.board[row][col] = "X"
            else:
                print("spot taken!")

def computer_move(game):
    empty = game.empty_cells()
    if empty:
        row, col = random.choice(empty)
        game.board[row][col] = "O"
        
# pygame setup
pygame.init()
WIDTH, HEIGHT = 600, 600
cell_size = 200
game = GameBoard()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

player_turn  = True
current_symbol = ""
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif player_turn and event.type == pygame.MOUSEBUTTONDOWN:
            player_move(game, cell_size)
            current_symbol = "X"
            player_turn = False
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("grey")

    # RENDER YOUR GAME HERE
    for i, row in enumerate(game.board):
        for j, col in enumerate(row):
            if game.board[i][j] == "X":
                game.X_draw(screen, i, j, cell_size)
            elif game.board[i][j] == "O":
                game.O_draw(screen, i, j, cell_size)
                
    if game.win_conditions(current_symbol):
        print(f"The winner is {current_symbol}! ")   
        pygame.time.delay(3000) 
        break

    if len(game.empty_cells()) == 0:
        print("It's a draw! ")
        pygame.time.delay(3000)
        break

    if not player_turn:
        computer_move(game)
        current_symbol = "O"
        player_turn = True

    game.draw_grid(screen, cell_size)
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()