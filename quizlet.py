import csv
import os

FILENAME = "word.csv"

def add_words():
    file_exists = os.path.isfile(FILENAME)

    with open(FILENAME, "a", newline="") as csvfile:
        fieldnames = ["word", "translation"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        while True:
            word = input("Add a word: ").strip()
            translation = input("Add its translation: ").strip()
            writer.writerow({"word": word,"translation": translation})
            more = input("Add another word? (Y/n): ").strip().lower()
            if more != "y":
                break
                
def read_words():
    if not os.path.isfile(FILENAME):
        print("No words saved yet.")
        return

    with open(FILENAME, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        print("\nSaved words:")
        for row in reader:
            print(f"{row['word']} → {row['translation']}")

def main():
    while True:
        print("\n1. Add words")
        print("2. View words")
        print("3. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_words()
        elif choice == "2":
            read_words()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
