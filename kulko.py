import random

class Board:
    def __init__(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
    
    def print_board(self):
        for i, row in enumerate(self.board):
            print(" | ".join(row))
            if i < 2:
                print("--+---+--")

    def win_conditions(self, symbol):
        for i in range(3):
            if all(self.board[i][j] == symbol for j in range(3)) or all(self.board[j][i] == symbol for j in range(3)):
                return True

        if all(self.board[i][i] == symbol for i in range(3)) or all(self.board[i][2-i] == symbol for i in range(3)):
            return True
        return False
    
board = Board()

def computer_move(symbol):
    pass

def player_move(symbol):
    pass

def is_input_valid(player_symbol):
    while player_symbol not in ("X", "O"):
        player_symbol = input("Chose symbol ('X' or 'O') ").upper()
    return player_symbol

# def is_valid_move():
#     empty_celles = [(i, j) for i in range(3) for j in range(3) if board.board[i][j] == " "]
#     return empty_celles

def main():
    board.print_board()

    player_symbol = is_input_valid(input("Chose symbol ('X' or 'O') ").upper())
    computer_symbol = "O" if player_symbol == "X" else "X"

    turn = "player" if player_symbol == "X" else "computer"
    
    while True:

        if turn == "player":
            player_move(player_symbol)
            computer_move(computer_symbol)
        else:
            computer_move(computer_symbol)
            player_move(player_symbol)

        current_symbol = player_symbol if turn == "player" else computer_symbol
        if board.win_conditions(current_symbol):
            print(f"{current_symbol} is a winner ")
            break

main()