import time

def countdown(seconds):
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        timer = f"{mins:02}:{secs:02}"
        print(timer, end="\r")
        time.sleep(1)
        seconds -= 1
    print("Time's up!")

def main():
    print("Countdown Timer")
    while True:
        try:
            total = int(input("\nEnter time in seconds: "))
            if total <= 0:
                print("Please enter a positive number.")
                continue
        except ValueError:
            print("Invalid input, enter a number.")
            continue

        countdown(total)

        again = input("Do you want to start another timer? (y/n): ").strip().lower()
        if again != "y":
            print("Exiting Countdown Timer.")
            break

if __name__ == "__main__":
    main()
