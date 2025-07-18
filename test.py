import random

WORDS = ['python', 'banana', 'keyboard', 'puzzle', 'developer']

def scramble(word):
    word = list(word)
    random.shuffle(word)
    return ''.join(word)

def play_game():
    word = random.choice(WORDS)
    scrambled = scramble(word)
    print("Unscramble the word:", scrambled)

    attempts = 3
    while attempts > 0:
        guess = input("Your guess: ").strip().lower()
        if guess == word:
            print("🎉 Correct!")
            return
        else:
            print("❌ Try again.")
            attempts -= 1
    print(f"Out of attempts! The word was: {word}")

if __name__ == "__main__":
    play_game()