import random

def number_guessing_game():
    print(" Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100...")
    
    secret_number = random.randint(1, 100)
    attempts = 0
    max_attempts = 7

    while attempts < max_attempts:
        try:
            guess = int(input(f"\nAttempt {attempts + 1}/{max_attempts} - Enter your guess: "))
        except ValueError:
            print(" Please enter a valid number!")
            continue

        attempts += 1

        if guess < secret_number:
            print("Too low! Try again.")
        elif guess > secret_number:
            print(" Too high! Try again.")
        else:
            print(f" Correct! The number was {secret_number}. You guessed it in {attempts} tries!")
            break
    else:
        print(f"\n Out of attempts! The number was {secret_number}.")

if __name__ == "__main__":
    number_guessing_game()
