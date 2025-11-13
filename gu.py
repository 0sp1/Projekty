import random
import json
import os

class GuessingGame:
    def __init__(self, score_file="score.json"):
        self.score_file = score_file
        self.scores = {}
        self.player_name = ""
        self.load_scores()

    def load_scores(self):
        if os.path.exists(self.score_file):
            with open(self.score_file, "r") as f:
                try:
                    self.scores = json.load(f)
                except json.JSONDecodeError:
                    self.scores = {}

    def save_scores(self):
        with open(self.score_file, "w") as f:
            json.dump(self.scores, f, indent=4)

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

    def get_player(self):
        print("\n=== Welcome to the Number Guessing Game ===")
        name = input("Enter your player name: ").strip()
        if not name:
            name = "Guest"
        self.player_name = name
        if name not in self.scores:
            self.scores[name] = {"best_score": {}}
        print(f"Hello, {name}! Let's get started.")

    def give_hint(self, number, upper_limit, guess, attempts):
        # Provide hints at certain attempt thresholds
        if attempts == 3:
            print(f"Hint: The number is {'even' if number % 2 == 0 else 'odd'}.")
        elif attempts == 5:
            lower_bound = max(1, number - upper_limit // 10)
            upper_bound = min(upper_limit, number + upper_limit // 10)
            print(f"Hint: It’s between {lower_bound} and {upper_bound}.")
        elif attempts == 7:
            if number > upper_limit / 2:
                print("Hint: The number is in the upper half of the range.")
            else:
                print("Hint: The number is in the lower half of the range.")

    def play(self):
        self.get_player()
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
                    print(f"Correct! You guessed it in {attempts} attempts.")
                    player_scores = self.scores[self.player_name]["best_score"]
                    best = player_scores.get(difficulty)
                    if best is None or attempts < best:
                        player_scores[difficulty] = attempts
                        self.save_scores()
                        print(f"New best score for {difficulty} mode, {self.player_name}!")
                    else:
                        print(f"Best score for {difficulty}: {best} attempts.")
                    break

                self.give_hint(number, upper_limit, guess, attempts)

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
