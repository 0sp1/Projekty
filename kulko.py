import random
#create 3d arry for a grid and prints board 
class Board:
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
    
    def print_board(self):
        for i, row in enumerate(self.board):
            print(f"{" | ".join(row)}")
            if i < 2:
                print("--+---+--")
game = Board()

#print game board
def main():
    game.print_board()

    player_symbol = input("Chose symbol ('X' or 'O')").upper()

    while player_symbol not in ("X", "O"):
        player_symbol = input("Chose symbol ('X' or 'O')").upper()
    
    turn = "player" if player_symbol == "X" else "computer"
    

    if turn == "player":
        player_move()
    else:
        computer_move()
        turn = "player"

def computer_move():
    pass
def player_move():
    pass



main()