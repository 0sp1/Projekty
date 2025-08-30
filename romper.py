import random

def generate_sequence():
    start = random.randint(1, 10)
    step = random.randint(2, 5)
    length = 5
    sequence = [start + step * i for i in range(length)]
    return sequence

def play():
    seq = generate_sequence()
    missing_index = random.randint(0, len(seq) - 1)
    answer = seq[missing_index]
    puzzle = seq[:]
    puzzle[missing_index] = "?"

    print("Number Puzzle Game")
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
