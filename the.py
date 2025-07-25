import time
import threading

running = False
start_time = 0
elapsed_time = 0

def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 100)
    return f"{mins:02}:{secs:02}.{millis:02}"

def stopwatch():
    global running, start_time, elapsed_time
    while running:
        time.sleep(0.1)
        current_time = time.time()
        elapsed_time = current_time - start_time
        print(f"\r⏱️ {format_time(elapsed_time)}", end="")

def start():
    global running, start_time
    if not running:
        running = True
        start_time = time.time() - elapsed_time
        threading.Thread(target=stopwatch, daemon=True).start()
        print("▶️ Started")

def stop():
    global running
    if running:
        running = False
        print(f"\n⏹️ Stopped at {format_time(elapsed_time)}")

def reset():
    global elapsed_time, running
    if not running:
        elapsed_time = 0
        print("🔄 Reset to 00:00.00")

def main():
    print("⌚ Simple Stopwatch")
    print("Commands: start, stop, reset, exit")
    while True:
        cmd = input("\n> ").strip().lower()
        if cmd == "start":
            start()
        elif cmd == "stop":
            stop()
        elif cmd == "reset":
            reset()
        elif cmd == "exit":
            stop()
            print("👋 Goodbye!")
            break
        else:
            print("⚠️ Unknown command.")

if __name__ == "__main__":
    main()

