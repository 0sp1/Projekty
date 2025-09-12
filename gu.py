import random
import json
import os

class GuessingGame:
    def __init__(self, score_file="score.json"):
        self.score_file = score_file
        self.best_score = None
        self.load_score()

    def load_score(self):
        if os.path.exists(self.score_file):
            with open(self.score_file, "r") as f:
                try:
                    data = json.load(f)
                    self.best_score = data.get("best_score", None)
                except json.JSONDecodeError:
                    self.best_score = None

    def save_score(self):
        with open(self.score_file, "w") as f:
            json.dump({"best_score": self.best_score}, f, indent=4)

    def play(self):
        print("Welcome to the Number Guessing Game!")
        print("I’m thinking of a number between 1 and 100.")
        number = random.randint(1, 100)
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
                    print(f"Correct! You guessed it in {attempts} attempts.")
                    if self.best_score is None or attempts < self.best_score:
                        self.best_score = attempts
                        self.save_score()
                        print("New best score!")
                    else:
                        print(f"Best score so far: {self.best_score}")
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
