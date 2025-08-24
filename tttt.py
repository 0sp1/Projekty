import time

def stopwatch():
    print("Simple Stopwatch")
    print("Commands: 'start', 'stop', 'reset', 'exit'")

    running = False
    start_time = 0
    elapsed = 0

    while True:
        command = input("\nEnter command: ").strip().lower()

        if command == "start":
            if not running:
                running = True
                start_time = time.time() - elapsed
                print("Stopwatch started.")
            else:
                print("Stopwatch is already running.")

        elif command == "stop":
            if running:
                running = False
                elapsed = time.time() - start_time
                print(f"Stopped at {elapsed:.2f} seconds.")
            else:
                print("Stopwatch is not running.")

        elif command == "reset":
            running = False
            start_time = 0
            elapsed = 0
            print("Stopwatch reset to 0.")

        elif command == "exit":
            if running:
                elapsed = time.time() - start_time
            print(f"Final time: {elapsed:.2f} seconds.")
            print("Goodbye.")
            break

        else:
            print("Invalid command. Use 'start', 'stop', 'reset', or 'exit'.")

if __name__ == "__main__":
    stopwatch()
