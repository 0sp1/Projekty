import time
import random

sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "Typing is a useful skill for everyone.",
    "Practice makes perfect, especially in coding.",
    "Python is fun and easy to learn.",
    "A journey of a thousand miles begins with a single step."
]

def get_random_sentence():
    return random.choice(sentences)

def calculate_speed(start, end, text):
    time_taken = end - start
    words = len(text.split())
    wpm = (words / time_taken) * 60
    return round(wpm, 2), round(time_taken, 2)

def main():
    print("⌨️ Typing Speed Test")
    while True:
        input("\nPress Enter to start...")
        sentence = get_random_sentence()
        print("\nType this:")
        print(f"> {sentence}")

        start_time = time.time()
        typed = input("\nYour input:\n> ")
        end_time = time.time()

        wpm, seconds = calculate_speed(start_time, end_time, typed)
        print(f"\n⏱️ Time: {seconds} seconds")
        print(f"💨 Speed: {wpm} WPM")

        if typed.strip() == sentence.strip():
            print("✅ Perfect typing!")
        else:
            print("❌ You made some mistakes.")

        again = input("\nTry again? (y/n): ").lower()
        if again != 'y':
            print("👋 Thanks for playing!")
            break

if __name__ == "__main__":
    main()
