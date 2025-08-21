import random
import time

def roll_dice(sides=6):
    return random.randint(1, sides)

def main():
    print(" Welcome to the Dice Rolling Simulator!")
    print("You can roll a dice with any number of sides.\n")

    while True:
        try:
            sides = int(input("Enter number of sides on the dice (e.g., 6): "))
            if sides < 2:
                print(" A dice must have at least 2 sides!")
                continue
        except ValueError:
            print(" Please enter a valid number.")
            continue

        rolls = int(input("How many times do you want to roll? "))
        print("\nRolling the dice...\n")
        time.sleep(1)

        results = [roll_dice(sides) for _ in range(rolls)]
        for i, r in enumerate(results, 1):
            print(f"Roll {i}:  {r}")

        print(f"\nSummary: Min={min(results)}, Max={max(results)}, Avg={sum(results)/len(results):.2f}")

        again = input("\nDo you want to roll again? (y/n): ").lower()
        if again != "y":
            print(" Thanks for playing Dice Simulator!")
            break

if __name__ == "__main__":
    main()
