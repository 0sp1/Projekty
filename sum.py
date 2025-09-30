import random
import json
import os

class Highscore:
    def __init__(self, filename="highscore.json"):
        self.filename = filename
        self.score = self.load_score()

    def load_score(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                return json.load(f).get("highscore", None)
        return None

    def save_score(self, score):
        if self.score is None or score < self.score:
            self.score = score
            with open(self.filename, "w") as f:
                json.dump({"highscore": self.score}, f)
            print(f"New highscore: {self.score} attempts!")
        else:
            print(f"Highscore remains: {self.score} attempts.")

class GuessingGame:
    def __init__(self, min_val=1, max_val=100):
        self.number = random.randint(min_val, max_val)
        self.attempts = 0
        self.min_val = min_val
        self.max_val = max_val
        self.highscore = Highscore()

    def play(self):
        print(f"\nWelcome to the Number Guessing Game!")
        print(f"I'm thinking of a number between {self.min_val} and {self.max_val}.")
        print("Try to guess it in the fewest attempts.\n")

        while True:
            try:
                guess = int(input("Enter your guess: "))
                self.attempts += 1

                if guess < self.number:
                    print("Too low!")
                elif guess > self.number:
                    print("Too high!")
                else:
                    print(f"Correct! You guessed it in {self.attempts} attempts.")
                    self.highscore.save_score(self.attempts)
                    break
            except ValueError:
                print("Please enter a valid number.")

def choose_difficulty():
    print("\nSelect difficulty:")
    print("1. Easy (1–50)")
    print("2. Medium (1–100)")
    print("3. Hard (1–200)")
    while True:
        choice = input("Choose difficulty: ")
        if choice == "1":
            return 1, 50
        elif choice == "2":
            return 1, 100
        elif choice == "3":
            return 1, 200
        else:
            print("Invalid choice. Try again.")

def menu():
    while True:
        print("\n--- Main Menu ---")
        print("1. Play Game")
        print("2. View Highscore")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            min_val, max_val = choose_difficulty()
            game = GuessingGame(min_val, max_val)
            game.play()
        elif choice == "2":
            hs = Highscore()
            if hs.score is None:
                print("No highscore yet. Play a game first!")
            else:
                print(f"Current highscore: {hs.score} attempts.")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    menu()
