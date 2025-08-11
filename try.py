import time

def stopwatch():
    print("\n--- Stopwatch ---")
    input("Press Enter to start...")
    start = time.time()
    try:
        while True:
            elapsed = time.time() - start
            print(f"\rElapsed: {elapsed:.2f} sec", end="")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopped at", f"{time.time() - start:.2f} sec")

def timer():
    print("\n--- Countdown Timer ---")
    try:
        seconds = int(input("Enter seconds: "))
    except ValueError:
        print("Invalid number.")
        return
    for remaining in range(seconds, 0, -1):
        print(f"\rTime left: {remaining} sec", end="")
        time.sleep(1)
    print("\nTime's up! ⏰")

def menu():
    print("\n=== Stopwatch & Timer ===")
    print("1. Stopwatch")
    print("2. Countdown Timer")
    print("3. Exit")

def main():
    while True:
        menu()
        choice = input("Choose an option: ")
        if choice == "1":
            stopwatch()
        elif choice == "2":
            timer()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
