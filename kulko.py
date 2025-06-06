import random

class Board:
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
    
    def print_board(self):
        for i, row in enumerate(self.board):
            print(" | ".join(row))
            if i < 2:
                print("--+---+--")
    def win_conditions(self):
        pass

board = Board()

def computer_move(symbol):
    print(symbol)

def player_move(symbol):
    print(symbol)

def is_input_valid(player_symbol):
    while player_symbol not in ("X", "O"):
        player_symbol = input("Chose symbol ('X' or 'O')").upper()
    return player_symbol

def main():
    board.print_board()

    player_symbol = is_input_valid(input("Chose symbol ('X' or 'O')").upper())
    computer_symbol = "O" if player_symbol == "X" else "X"

    turn = "player" if player_symbol == "X" else "computer"

    while True:

        if turn == "player":
            player_move(player_symbol)
            computer_move(computer_symbol)
        else:
            computer_move(computer_symbol)
            player_move(player_symbol)

main()