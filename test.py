
import random
import os

HIGH_SCORE_FILE = "high_score.txt"

def load_high_score():
    if not os.path.exists(HIGH_SCORE_FILE):
        return None
    with open(HIGH_SCORE_FILE, "r") as file:
        try:
            return int(file.read().strip())
        except ValueError:
            return None

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))

def get_valid_guess():
    while True:
        try:
            guess = int(input("Enter your guess (1-100): "))
            if 1 <= guess <= 100:
                return guess
            else:
                print("Number must be between 1 and 100.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def play_game():
    secret = random.randint(1, 100)
    attempts = 0
    print("I'm thinking of a number between 1 and 100.")

    while True:
        guess = get_valid_guess()
        attempts += 1
        if guess < secret:
            print("Too low!")
        elif guess > secret:
            print("Too high!")
        else:
            print(f"Correct! The number was {secret}.")
            print(f"You guessed it in {attempts} attempts.")
            return attempts

def main_menu():
    print("\n--- Number Guessing Game ---")
    print("1. Play")
    print("2. View High Score")
    print("3. Exit")

def main():
    high_score = load_high_score()

    while True:
        main_menu()
        choice = input("Choose an option: ")
        if choice == "1":
            score = play_game()
            if high_score is None or score < high_score:
                print("New high score!")
                save_high_score(score)
                high_score = score
        elif choice == "2":
            if high_score is None:
                print("No high score yet.")
            else:
                print(f"High score: {high_score} attempts")
        elif choice == "3":
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
