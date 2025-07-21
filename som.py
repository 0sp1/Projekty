import random
import time

def welcome():
    print("🎯 Welcome to the Number Guessing Game!")
    print("Choose a difficulty level:")
    print("1. Easy (1–10)")
    print("2. Medium (1–50)")
    print("3. Hard (1–100)")

def get_range(choice):
    if choice == '1':
        return 1, 10
    elif choice == '2':
        return 1, 50
    elif choice == '3':
        return 1, 100
    else:
        print("Invalid choice. Defaulting to Easy.")
        return 1, 10

def play_game():
    welcome()
    choice = input("Enter your choice (1/2/3): ")
    low, high = get_range(choice)
    number = random.randint(low, high)
    attempts = 0
    score = 100

    print(f"\nGuess a number between {low} and {high}!")

    while True:
        try:
            guess = int(input("Your guess: "))
            attempts += 1
            if guess < number:
                print("🔻 Too low!")
                score -= 5
            elif guess > number:
                print("🔺 Too high!")
                score -= 5
            else:
                print(f"✅ Correct! You guessed it in {attempts} attempts.")
                break
        except ValueError:
            print("⚠️ Please enter a valid number.")

    print(f"🎉 Your score: {max(score, 0)}")
    return input("Play again? (y/n): ").lower() == 'y'

def main():
    while True:
        if not play_game():
            print("👋 Thanks for playing!")
            break
        time.sleep(1)

if __name__ == "__main__":
    main()
