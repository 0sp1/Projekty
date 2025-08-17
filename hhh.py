import random
import time

def choose_level():
    print("🎮 Welcome to the Number Guessing Game!")
    print("Choose a difficulty level:")
    print("1. Easy (1–10, 5 attempts)")
    print("2. Medium (1–50, 7 attempts)")
    print("3. Hard (1–100, 10 attempts)")

    while True:
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice == "1":
            return 10, 5
        elif choice == "2":
            return 50, 7
        elif choice == "3":
            return 100, 10
        else:
            print("❌ Invalid choice, try again.")

def play_game():
    max_num, attempts = choose_level()
    secret = random.randint(1, max_num)
    print(f"\nI'm thinking of a number between 1 and {max_num}.")
    print(f"You have {attempts} attempts. Good luck!\n")

    for i in range(1, attempts + 1):
        try:
            guess = int(input(f"Attempt {i}: Enter your guess → "))
        except ValueError:
            print("❌ Please enter a valid number!")
            continue

        if guess == secret:
            print(f"✅ Correct! The number was {secret}.")
            print(f"You guessed it in {i} attempts. 🎉")
            break
        elif guess < secret:
            print("🔼 Too low!")
        else:
            print("🔽 Too high!")

        if i == attempts:
            print(f"\n😢 Out of attempts! The number was {secret}.")
        else:
            hint = "even" if secret % 2 == 0 else "odd"
            print(f"💡 Hint: The number is {hint}.\n")
            time.sleep(0.5)

def main():
    while True:
        play_game()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("👋 Thanks for playing! Goodbye.")
            break

if __name__ == "__main__":
    main()
