import random

WORDS = ["python", "hangman", "computer", "programming",
         "openai", "science", "wizard", "galaxy", "puzzle"]

def choose_word():
    return random.choice(WORDS)

def display(word, guessed):
    return " ".join(c if c in guessed else "_" for c in word)

def play():
    word = choose_word()
    guessed = set()
    attempts = 6

    print("🎮 Welcome to Hangman!")
    print("Guess the word before you run out of attempts.\n")

    while attempts > 0:
        print(display(word, guessed))
        print(f"Attempts left: {attempts}")
        guess = input("Enter a letter: ").lower().strip()

        if not guess.isalpha() or len(guess) != 1:
            print(" Please enter a single letter.\n")
            continue
        if guess in guessed:
            print(" Already guessed that letter.\n")
            continue

        guessed.add(guess)
        if guess in word:
            print(" Correct!\n")
            if all(c in guessed for c in word):
                print(f" You win! The word was '{word}'.")
                break
        else:
            attempts -= 1
            print("Wrong guess!\n")

    else:
        print(f" Game Over! The word was '{word}'.")

def main():
    while True:
        play()
        again = input("\nPlay again? (y/n): ").lower()
        if again != "y":
            print(" Thanks for playing Hangman!")
            break

if __name__ == "__main__":
    main()

