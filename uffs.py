import random

def number_guessing_game():
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    print("You have 7 tries to guess it correctly.\n")

    number_to_guess = random.randint(1, 100)
    attempts = 7

    for attempt in range(1, attempts + 1):
        try:
            guess = int(input(f"Attempt {attempt}: Enter your guess: "))
        except ValueError:
            print("Please enter a valid number!")
            continue

        if guess < number_to_guess:
            print("Too low! Try again.\n")
        elif guess > number_to_guess:
            print("Too high! Try again.\n")
        else:
            print(f"🎉 Congratulations! You guessed it in {attempt} tries!")
            break
    else:
        print(f"😢 Sorry, you're out of tries. The number was {number_to_guess}.")

if __name__ == "__main__":
    number_guessing_game()
