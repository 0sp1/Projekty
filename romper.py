import random

def generate_sequence(difficulty):
    if difficulty == "easy":
        start = random.randint(1, 10)
        step = random.randint(1, 3)
        length = 4
    elif difficulty == "medium":
        start = random.randint(1, 20)
        step = random.randint(2, 5)
        length = 5
    else:  # hard
        start = random.randint(1, 50)
        step = random.randint(5, 10)
        length = random.randint(6, 7)

    sequence = [start + step * i for i in range(length)]
    return sequence

def choose_difficulty():
    while True:
        print("\nChoose difficulty level:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice == "1":
            return "easy"
        elif choice == "2":
            return "medium"
        elif choice == "3":
            return "hard"
        else:
            print("Invalid input. Please choose 1, 2, or 3.")

def play():
    difficulty = choose_difficulty()
    seq = generate_sequence(difficulty)
    missing_index = random.randint(0, len(seq) - 1)
    answer = seq[missing_index]
    puzzle = seq[:]
    puzzle[missing_index] = "?"

    print("\nNumber Puzzle Game")
    print("Find the missing number in the sequence:")
    print(" ".join(str(x) for x in puzzle))

    attempts = 3
    while attempts > 0:
        try:
            guess = int(input("Your guess: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if guess == answer:
            print("Correct! You solved the puzzle.")
            return
        else:
            attempts -= 1
            print(f"Wrong guess. Attempts left: {attempts}")

    print(f"Out of attempts! The missing number was {answer}.")

def main():
    while True:
        play()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing Number Puzzle!")
            break

if __name__ == "__main__":
    main()
