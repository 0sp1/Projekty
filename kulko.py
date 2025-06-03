def print_board():
    game_board = [["x" for _ in range(3)] for _ in range(3)]
    game_board[1][1] = "O"
    print(f" {game_board[0][0]} | {game_board[0][1]} | {game_board[0][2]} ")
    print("---+---+---")
    print(f" {game_board[1][0]} | {game_board[1][1]} | {game_board[2][2]} ")
    print("---+---+---")
    print(f" {game_board[2][0]} | {game_board[2][1]} | {game_board[2][2]} ")
    

def board_move(user_input):
    pass
print_board()