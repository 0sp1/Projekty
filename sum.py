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
    def __init__(self):
        self.number = random.randint(1, 100)
        self.attempts = 0
        self.highscore = Highscore()

    def play(self):
        print("Welcome to the Number Guessing Game!")
        print("I'm thinking of a number between 1 and 100.")
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

def menu():
    while True:
        print("\n1. Play Game")
        print("2. View Highscore")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            game = GuessingGame()
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
