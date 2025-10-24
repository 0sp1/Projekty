import time

def stopwatch():
    print("Multi-Mode Timer")
    print("Commands: 'start', 'stop', 'reset', 'lap', 'mode', 'exit'")
    print("Modes: Stopwatch (count up) or Countdown (count down)")

    running = False
    mode = "stopwatch"  # can be 'stopwatch' or 'countdown'
    start_time = 0
    elapsed = 0
    countdown_time = 0
    laps = []

    while True:
        command = input("\nEnter command: ").strip().lower()

        if command == "mode":
            if running:
                print("Stop the timer before changing modes.")
                continue

            if mode == "stopwatch":
                mode = "countdown"
                while True:
                    try:
                        countdown_time = float(input("Enter countdown time (in seconds): "))
                        break
                    except ValueError:
                        print("Please enter a valid number.")
                elapsed = countdown_time
                print(f"Switched to Countdown mode ({countdown_time} seconds).")
            else:
                mode = "stopwatch"
                elapsed = 0
                print("Switched to Stopwatch mode.")

        elif command == "start":
            if not running:
                running = True
                start_time = time.time()
                print(f"{mode.capitalize()} started.")
            else:
                print("Timer is already running.")

        elif command == "stop":
            if running:
                running = False
                if mode == "stopwatch":
                    elapsed += time.time() - start_time
                    print(f"Stopped at {elapsed:.2f} seconds.")
                else:  # countdown
                    elapsed = countdown_time - (time.time() - start_time)
                    if elapsed < 0:
                        elapsed = 0
                    print(f"Countdown stopped at {elapsed:.2f} seconds remaining.")
            else:
                print("Timer is not running.")

        elif command == "lap":
            if mode != "stopwatch":
                print("Lap feature is only available in Stopwatch mode.")
                continue

            if running:
                lap_time = time.time() - start_time + elapsed
                laps.append(lap_time)
                print(f"Lap {len(laps)}: {lap_time:.2f} seconds")
            else:
                print("Start the stopwatch to record laps.")

        elif command == "reset":
            running = False
            start_time = 0
            elapsed = 0
            laps.clear()
            print("Timer reset to 0.")

        elif command == "exit":
            if running:
                if mode == "stopwatch":
                    elapsed += time.time() - start_time
                else:
                    elapsed = countdown_time - (time.time() - start_time)
                    if elapsed < 0:
                        elapsed = 0
            print(f"Final time: {elapsed:.2f} seconds.")
            if laps:
                print("Lap times:")
                for i, lap in enumerate(laps, 1):
                    print(f"  Lap {i}: {lap:.2f} seconds")
            print("Goodbye.")
            break

        else:
            print("Invalid command. Use 'start', 'stop', 'reset', 'lap', 'mode', or 'exit'.")

if __name__ == "__main__":
    stopwatch()
