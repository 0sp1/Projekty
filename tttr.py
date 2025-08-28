import random

WORDS = ["python", "developer", "programming", "keyboard", "computer",
         "variable", "function", "algorithm", "project", "syntax"]

def scramble_word(word):
    scrambled = list(word)
    random.shuffle(scrambled)
    return "".join(scrambled)

def play():
    word = random.choice(WORDS)
    scrambled = scramble_word(word)
    print("Word Scramble Game")
    print("Unscramble the letters to form a valid word.")
    print("Scrambled word:", scrambled)

    attempts = 3
    while attempts > 0:
        guess = input("Your guess: ").strip().lower()
        if guess == word:
            print("Correct! You guessed the word.")
            return
        else:
            attempts -= 1
            print(f"Wrong guess. Attempts left: {attempts}")

    print(f"Out of attempts! The word was '{word}'.")

def main():
    while True:
        play()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing Word Scramble!")
            break

if __name__ == "__main__":
    main()
