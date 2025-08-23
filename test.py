import random
import time

jokes = [
    "Why don’t programmers like nature? It has too many bugs. ",
    "Why do Java developers wear glasses? Because they don’t see sharp. ",
    "How many programmers does it take to change a light bulb? None, that's a hardware problem. ",
    "Why was the computer cold? It forgot to close Windows. ",
    "Why did the Python programmer go broke? Because his code had too many 'except' blocks. ",
    "What do you call 8 hobbits? A hobbyte. ",
    "Why was the math book sad? It had too many problems. ",
    "Why did the scarecrow win an award? Because he was outstanding in his field. "
]

def get_joke():
    return random.choice(jokes)

def main():
    print(" Welcome to the Random Joke Generator! ")
    while True:
        input("\nPress ENTER for a joke...")
        joke = get_joke()
        print("\n" + joke)
        time.sleep(1)

        again = input("\nWant another one? (y/n): ").lower()
        if again != "y":
            print("\n Thanks for laughing with me!")
            break

if __name__ == "__main__":
    main()
