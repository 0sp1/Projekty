import random

class Board:
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
    
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
game_board = board.board

def empty_cells():
    empty_celles = [(i, j) for i in range(3) for j in range(3) if game_board[i][j] == " "]
    return empty_celles

def computer_move(symbol):
    row, col = random.choice(empty_cells())
    game_board[row][col] = symbol

def player_move(symbol):
    positions = {
        "1":(0,0), "2":(0,1), "3":(0,2),
        "4":(1,0), "5":(1,1), "6":(1,2),
        "7":(2,0), "8":(2,1), "9":(2,2),
    }
    while True:
        user_input = input("Chose a field (1-9) ")
        if user_input in positions:
            row, col = positions.get(user_input)
            if (row, col) in empty_cells():
                game_board[row][col] = symbol
                break
            else:
                print("Position already taken! ")
        else:
            print("Invalid input")
            
def is_input_valid(player_symbol):
    while player_symbol not in ("X", "O"):
        player_symbol = input("Chose symbol ('X' or 'O') ").upper()
    return player_symbol

def main():
    board.print_board()

    player_symbol = is_input_valid(input("Chose symbol ('X' or 'O') ").upper())
    computer_symbol = "O" if player_symbol == "X" else "X"

    turn = "player" if player_symbol == "X" else "computer"
    while True:
        if turn == "player":
            player_move(player_symbol)
        else:
            computer_move(computer_symbol)

        current_symbol = player_symbol if turn == "player" else computer_symbol
        board.print_board()

        if board.win_conditions(current_symbol):
            print(f"{current_symbol} is a winner ")
            break
        if len(empty_cells()) == 0:
            print("It's a draw")
            break
        
        turn = "computer" if turn == "player" else "player"
main()