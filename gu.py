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