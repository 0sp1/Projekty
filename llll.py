import random
import time

choices = ["rock", "paper", "scissors"]

def get_computer_choice():
    return random.choice(choices)

def get_winner(player, computer):
    if player == computer:
        return "draw"
    if (player == "rock" and computer == "scissors") or \
       (player == "paper" and computer == "rock") or \
       (player == "scissors" and computer == "paper"):
        return "player"
    return "computer"

def play_round():
    player = input(" Choose rock, paper, or scissors: ").lower().strip()
    if player not in choices:
        print(" Invalid choice! Try again.\n")
        return None

    computer = get_computer_choice()
    time.sleep(0.5)
    print(f"💻 Computer chose: {computer}")

    winner = get_winner(player, computer)
    if winner == "draw":
        print(" It's a draw!\n")
        return "draw"
    elif winner == "player":
        print(" You win!\n")
        return "player"
    else:
        print(" Computer wins!\n")
        return "computer"

def main():
    print("🎮 Welcome to Rock–Paper–Scissors!")
    score = {"player": 0, "computer": 0, "draw": 0}

    while True:
        result = play_round()
        if result:
            score[result] += 1

        print(f" Score → You: {score['player']} | Computer: {score['computer']} | Draws: {score['draw']}")

        again = input("Play again? (y/n): ").lower()
        if again != "y":
            print("\n Thanks for playing! Final Score:")
            print(f"You: {score['player']} | Computer: {score['computer']} | Draws: {score['draw']}")
            break

if __name__ == "__main__":
    main()
