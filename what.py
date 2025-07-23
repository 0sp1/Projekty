import random

WORDS = ["python", "hangman", "programming", "challenge", "keyboard", "function"]
MAX_TRIES = 6

def choose_word():
    return random.choice(WORDS)

def display_progress(word, guessed):
    return " ".join(letter if letter in guessed else "_" for letter in word)

def play_game():
    word = choose_word()
    guessed = set()
    tries = 0

    print("🎮 Welcome to Hangman!")
    print(f"Word: {display_progress(word, guessed)}")

    while tries < MAX_TRIES:
        guess = input("Guess a letter: ").lower()
        if not guess.isalpha() or len(guess) != 1:
            print("⚠️ Enter a single letter.")
            continue

        if guess in guessed:
            print("🔁 Already guessed.")
            continue

        guessed.add(guess)

        if guess in word:
            print("✅ Correct!")
        else:
            tries += 1
            print(f"❌ Wrong! {MAX_TRIES - tries} tries left.")

        progress = display_progress(word, guessed)
        print(f"Word: {progress}")

        if "_" not in progress:
            print("🎉 You won!")
            break
    else:
        print(f"💀 You lost! The word was '{word}'.")

def main():
    while True:
        play_game()
        again = input("Play again? (y/n): ").lower()
        if again != 'y':
            print("👋 Thanks for playing!")
            break

if __name__ == "__main__":
    main()
