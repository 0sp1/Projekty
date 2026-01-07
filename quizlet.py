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
            writer.writerow({"word": word, "translation": translation})

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

def search_words():
    if not os.path.isfile(FILENAME):
        print("No words saved yet.")
        return

    query = input("Search for: ").strip().lower()
    found = False

    with open(FILENAME, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if query in row["word"].lower() or query in row["translation"].lower():
                print(f"{row['word']} → {row['translation']}")
                found = True

    if not found:
        print("No matching words found.")

def delete_word():
    if not os.path.isfile(FILENAME):
        print("No words saved yet.")
        return

    target = input("Enter the word to delete: ").strip().lower()
    rows = []
    deleted = False

    with open(FILENAME, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["word"].lower() != target:
                rows.append(row)
            else:
                deleted = True

    if not deleted:
        print("Word not found.")
        return

    with open(FILENAME, "w", newline="") as csvfile:
        fieldnames = ["word", "translation"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("Word deleted successfully.")

def main():
    while True:
        print("\n1. Add words")
        print("2. View words")
        print("3. Search words")
        print("4. Delete a word")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_words()
        elif choice == "2":
            read_words()
        elif choice == "3":
            search_words()
        elif choice == "4":
            delete_word()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
