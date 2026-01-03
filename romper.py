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
    return sequence, step


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


def play(score):
    difficulty = choose_difficulty()
    seq, step = generate_sequence(difficulty)
    missing_index = random.randint(0, len(seq) - 1)
    answer = seq[missing_index]
    puzzle = seq[:]
    puzzle[missing_index] = "?"

    print("\nNumber Puzzle Game")
    print("Find the missing number in the sequence:")
    print(" ".join(str(x) for x in puzzle))
    print("(Type 'hint' for a clue or 'quit' to exit this round)")

    attempts = 3
    used_hint = False

    while attempts > 0:
        guess = input("Your guess: ").strip().lower()

        if guess == "quit":
            print("You quit this round.")
            return score

        if guess == "hint":
            if not used_hint:
                print(f"💡 Hint: The numbers change by {step} each time.")
                used_hint = True
                continue
            else:
                print("You've already used your hint for this round.")
                continue

        try:
            guess = int(guess)
        except ValueError:
            print("Please enter a valid number.")
            continue

        if guess == answer:
            print("✅ Correct! You solved the puzzle.")
            score += 10
            print(f"Your score: {score}")
            return score
        else:
            attempts -= 1
            score -= 3
            print(f"❌ Wrong guess. Attempts left: {attempts}")
            print(f"Current score: {score}")

    print(f"Out of attempts! The missing number was {answer}.")
    return score


def main():
    score = 0
    while True:
        score = play(score)
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print(f"🏁 Final Score: {score}")
            print("Thanks for playing Number Puzzle!")
            break


if __name__ == "__main__":
    main()
