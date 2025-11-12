import random
import json
import os

class GuessingGame:
    def __init__(self, score_file="score.json"):
        self.score_file = score_file
        self.best_score = {}
        self.load_score()

    def load_score(self):
        if os.path.exists(self.score_file):
            with open(self.score_file, "r") as f:
                try:
                    data = json.load(f)
                    self.best_score = data.get("best_score", {})
                except json.JSONDecodeError:
                    self.best_score = {}

    def save_score(self):
        with open(self.score_file, "w") as f:
            json.dump({"best_score": self.best_score}, f, indent=4)

    def choose_difficulty(self):
        print("\nSelect Difficulty:")
        print("1. Easy (1–50)")
        print("2. Medium (1–100)")
        print("3. Hard (1–500)")
        while True:
            choice = input("Enter choice (1-3): ").strip()
            if choice == "1":
                return "Easy", 50
            elif choice == "2":
                return "Medium", 100
            elif choice == "3":
                return "Hard", 500
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

    def play(self):
        print("\nWelcome to the Number Guessing Game!")
        difficulty, upper_limit = self.choose_difficulty()
        print(f"\nI'm thinking of a number between 1 and {upper_limit}.")
        number = random.randint(1, upper_limit)
        attempts = 0

        while True:
            try:
                guess = int(input("Enter your guess: "))
                attempts += 1
                if guess < number:
                    print("Too low!")
                elif guess > number:
                    print("Too high!")
                else:
                    print(f"✅ Correct! You guessed it in {attempts} attempts.")
                    best = self.best_score.get(difficulty)
                    if best is None or attempts < best:
                        self.best_score[difficulty] = attempts
                        self.save_score()
                        print(f"🎉 New best score for {difficulty} mode!")
                    else:
                        print(f"Best score for {difficulty}: {best} attempts.")
                    break
            except ValueError:
                print("Please enter a valid number.")

def main():
    game = GuessingGame()
    while True:
        game.play()
        again = input("Play again? (y/n): ").lower()
        if again != "y":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
