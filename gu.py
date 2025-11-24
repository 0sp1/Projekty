import random
import json
import os
import time


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

    def show_leaderboard(self):
        print("\n=== GLOBAL LEADERBOARD ===")
        leaderboard = []

        for player, data in self.scores.items():
            for difficulty, score in data.get("best_score", {}).items():
                leaderboard.append((player, difficulty, score))

        if not leaderboard:
            print("No scores recorded yet.")
            return

        leaderboard.sort(key=lambda x: x[2])

        for i, entry in enumerate(leaderboard[:10], start=1):
            player, difficulty, score = entry
            print(f"{i}. {player} - {difficulty}: {score} attempts")

    def choose_mode(self):
        print("\nSelect Game Mode:")
        print("1. Normal (count attempts)")
        print("2. Timed (measure seconds)")

        while True:
            choice = input("Enter choice (1-2): ").strip()
            if choice == "1":
                return "Normal"
            if choice == "2":
                return "Timed"
            print("Invalid choice. Please enter 1 or 2.")

    def choose_difficulty(self):
        print("\nSelect Difficulty:")
        print("1. Easy (1–50)")
        print("2. Medium (1–100)")
        print("3. Hard (1–500)")

        while True:
            choice = input("Enter choice (1-3): ").strip()
            if choice == "1":
                return "Easy", 50
            if choice == "2":
                return "Medium", 100
            if choice == "3":
                return "Hard", 500
            print("Invalid choice.")

    def get_player(self):
        print("\n=== Welcome to the Number Guessing Game ===")

        name = input("Enter your player name: ").strip()
        if not name:
            name = "Guest"

        self.player_name = name

        if name not in self.scores:
            self.scores[name] = {"best_score": {}, "best_time": {}}

        print(f"Hello, {name}! Let's begin.")

    def give_hint(self, number, upper_limit, guess, attempts):
        if attempts == 3:
            print(f"Hint: The number is {'even' if number % 2 == 0 else 'odd'}.")
        elif attempts == 5:
            lower_bound = max(1, number - upper_limit // 10)
            upper_bound = min(upper_limit, number + upper_limit // 10)
            print(f"Hint: It’s between {lower_bound} and {upper_bound}.")
        elif attempts == 7:
            if number > upper_limit / 2:
                print("Hint: The number is in the upper half.")
            else:
                print("Hint: The number is in the lower half.")

    def play(self):
        self.get_player()

        if input("View leaderboard? (y/n): ").lower() == "y":
            self.show_leaderboard()

        game_mode = self.choose_mode()
        difficulty, upper_limit = self.choose_difficulty()

        print(f"\nI'm thinking of a number between 1 and {upper_limit}.")
        number = random.randint(1, upper_limit)

        attempts = 0
        start_time = time.time() if game_mode == "Timed" else None

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

                    if game_mode == "Timed":
                        elapsed = round(time.time() - start_time, 2)
                        print(f"⏱ Time taken: {elapsed} seconds")

                        best_time = self.scores[self.player_name]["best_time"].get(difficulty)

                        if best_time is None or elapsed < best_time:
                            self.scores[self.player_name]["best_time"][difficulty] = elapsed
                            print("New best time!")
                        else:
                            print(f"Best time: {best_time}s")

                    else:
                        player_scores = self.scores[self.player_name]["best_score"]
                        best = player_scores.get(difficulty)

                        if best is None or attempts < best:
                            player_scores[difficulty] = attempts
                            print("New best score!")
                        else:
                            print(f"Best score: {best} attempts.")

                    self.save_scores()
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
