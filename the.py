import random
import os

SCORE_FILE = "rps_score.txt"
CHOICES = ["rock", "paper", "scissors"]

def load_score():
    if not os.path.exists(SCORE_FILE):
        return {"wins": 0, "losses": 0, "ties": 0}
    with open(SCORE_FILE, "r") as file:
        data = file.read().strip().split(",")
        return {"wins": int(data[0]), "losses": int(data[1]), "ties": int(data[2])}

def save_score(score):
    with open(SCORE_FILE, "w") as file:
        file.write(f"{score['wins']},{score['losses']},{score['ties']}")

def get_user_choice():
    while True:
        choice = input("Rock, Paper, or Scissors? ").lower()
        if choice in CHOICES:
            return choice
        print("Invalid choice. Try again.")

def get_computer_choice():
    return random.choice(CHOICES)

def determine_winner(user, comp):
    if user == comp:
        return "tie"
    elif (user == "rock" and comp == "scissors") or \
         (user == "paper" and comp == "rock") or \
         (user == "scissors" and comp == "paper"):
        return "win"
    else:
        return "loss"

def display_score(score):
    print(f"Wins: {score['wins']} | Losses: {score['losses']} | Ties: {score['ties']}")

def main():
    score = load_score()
    print("=== Rock, Paper, Scissors ===")

    while True:
        user_choice = get_user_choice()
        comp_choice = get_computer_choice()
        print(f"Computer chose: {comp_choice}")

        result = determine_winner(user_choice, comp_choice)

        if result == "win":
            print("You win!")
            score["wins"] += 1
        elif result == "loss":
            print("You lose!")
            score["losses"] += 1
        else:
            print("It's a tie.")
            score["ties"] += 1

        save_score(score)
        display_score(score)

        if input("Play again? (y/n): ").lower() != "y":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
