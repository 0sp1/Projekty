import random, os
import copy

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
    
    def make_move(self, row, col, symbol):
        self.board[row][col] = symbol
    
    def undo_move(self, row, col):
        self.board[row][col] = " "

    def empty_cells(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == " "]

    def is_full(self):
        return all(self.board[i][j] != " " for i in range(3) for j in range(3))

def minimax(board, depth, is_maximizing, player_symbol, computer_symbol):
    if board.win_conditions(computer_symbol):
        return 10 - depth
    if board.win_conditions(player_symbol):
        return depth - 10
    if board.is_full():
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for (row, col) in board.empty_cells():
            board.make_move(row, col, computer_symbol)
            score = minimax(board, depth + 1, False, player_symbol, computer_symbol)
            board.undo_move(row, col)
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for (row, col) in board.empty_cells():
            board.make_move(row, col, player_symbol)
            score = minimax(board, depth + 1, True, player_symbol, computer_symbol)
            board.undo_move(row, col)
            best_score = min(score, best_score)
        return best_score

def computer_move(symbol, board, player_symbol):
    best_score = float('-inf')
    best_move = None

    for (row, col) in board.empty_cells():
        board.make_move(row, col, symbol)
        score = minimax(board, 0, False, player_symbol, symbol)
        board.undo_move(row, col)

        if score > best_score:
            best_score = score
            best_move = (row, col)

    if best_move:
        board.make_move(best_move[0], best_move[1], symbol)

def player_move(symbol, board):
    positions = {
        "1":(0,0), "2":(0,1), "3":(0,2),
        "4":(1,0), "5":(1,1), "6":(1,2),
        "7":(2,0), "8":(2,1), "9":(2,2),
    }
    while True:
        user_input = input("Choose a field (1-9): ")
        if user_input in positions:
            row, col = positions[user_input]
            if (row, col) in board.empty_cells():
                board.make_move(row, col, symbol)
                break
            else:
                print("Position already taken!")
        else:
            print("Invalid input")

def is_input_valid(player_symbol):
    while player_symbol not in ("X", "O"):
        player_symbol = input("Choose symbol ('X' or 'O'): ").upper()
    return player_symbol

def main():
    board = Board()
    board.print_board()

    player_symbol = is_input_valid(input("Choose symbol ('X' or 'O'): ").upper())
    computer_symbol = "O" if player_symbol == "X" else "X"

    turn = "player" if player_symbol == "X" else "computer"
    os.system("cls" if os.name == "nt" else "clear")
    
    while True:
        if turn == "player":
            player_move(player_symbol, board)
        else:
            computer_move(computer_symbol, board, player_symbol)

        os.system("cls" if os.name == "nt" else "clear")
        board.print_board()

        current_symbol = player_symbol if turn == "player" else computer_symbol
        if board.win_conditions(current_symbol):
            print(f"{current_symbol} wins!")
            break
        if board.is_full():
            print("It's a draw!")
            break

        turn = "computer" if turn == "player" else "player"

main()
