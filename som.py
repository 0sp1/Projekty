import sounddevice as sd
import wave
import os
from datetime import datetime

def record_audio(filename, duration=5, samplerate=44100):
    print(f"Recording for {duration} seconds...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=2, dtype='int16')
    sd.wait()
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(recording.tobytes())
    print(f"Saved recording as {filename}")

def list_recordings():
    files = [f for f in os.listdir() if f.endswith(".wav")]
    if not files:
        print("No recordings found.")
        return
    print("\n--- Recordings ---")
    for f in files:
        print(f)

def menu():
    print("\n=== Voice Recorder ===")
    print("1. Record audio")
    print("2. List recordings")
    print("3. Exit")

def main():
    while True:
        menu()
        choice = input("Choose: ")
        if choice == "1":
            try:
                duration = int(input("Duration in seconds: "))
            except ValueError:
                duration = 5
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recording_{timestamp}.wav"
            record_audio(filename, duration)
        elif choice == "2":
            list_recordings()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
