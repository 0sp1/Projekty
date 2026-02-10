import csv
import os
import random

FILENAME = "word.csv"

def load_words():
    if not os.path.isfile(FILENAME):
        return []
    with open(FILENAME, "r", newline="") as csvfile:
        return list(csv.DictReader(csvfile))

def save_words(words):
    with open(FILENAME, "w", newline="") as csvfile:
        fieldnames = ["word", "translation"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(words)

def add_words():
    words = load_words()
    existing = {row["word"].lower() for row in words}

    with open(FILENAME, "a", newline="") as csvfile:
        fieldnames = ["word", "translation"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not os.path.isfile(FILENAME) or not words:
            writer.writeheader()

        while True:
            word = input("Add a word: ").strip()
            if word.lower() in existing:
                print("Word already exists.")
            else:
                translation = input("Add its translation: ").strip()
                writer.writerow({"word": word, "translation": translation})
                existing.add(word.lower())

            more = input("Add another word? (Y/n): ").strip().lower()
            if more != "y":
                break

def read_words():
    words = load_words()
    if not words:
        print("No words saved yet.")
        return

    print("\nSaved words:")
    for row in words:
        print(f"{row['word']} → {row['translation']}")

def search_words():
    words = load_words()
    if not words:
        print("No words saved yet.")
        return

    query = input("Search for: ").strip().lower()
    found = False

    for row in words:
        if query in row["word"].lower() or query in row["translation"].lower():
            print(f"{row['word']} → {row['translation']}")
            found = True

    if not found:
        print("No matching words found.")

def delete_word():
    words = load_words()
    if not words:
        print("No words saved yet.")
        return

    target = input("Enter the word to delete: ").strip().lower()
    new_words = [row for row in words if row["word"].lower() != target]

    if len(new_words) == len(words):
        print("Word not found.")
        return

    save_words(new_words)
    print("Word deleted successfully.")

def edit_word():
    words = load_words()
    if not words:
        print("No words saved yet.")
        return

    target = input("Enter the word to edit: ").strip().lower()
    updated = False

    for row in words:
        if row["word"].lower() == target:
            new_word = input(f"New word (leave empty to keep '{row['word']}'): ").strip()
            new_translation = input(
                f"New translation (leave empty to keep '{row['translation']}'): "
            ).strip()

            if new_word:
                row["word"] = new_word
            if new_translation:
                row["translation"] = new_translation

            updated = True
            break

    if not updated:
        print("Word not found.")
        return

    save_words(words)
    print("Word updated successfully.")

def quiz_words():
    words = load_words()
    if not words:
        print("No words to quiz.")
        return

    print("\nQuiz mode (press Enter to quit)")
    while True:
        word = random.choice(words)
        answer = input(f"What is the translation of '{word['word']}'? ").strip()
        if answer == "":
            break
        if answer.lower() == word["translation"].lower():
            print("Correct")
        else:
            print(f"Wrong. Correct answer: {word['translation']}")

def statistics():
    words = load_words()
    if not words:
        print("No words saved yet.")
        return

    random_word = random.choice(words)
    print(f"Total words: {len(words)}")
    print(f"Random word: {random_word['word']} → {random_word['translation']}")

def main():
    while True:
        print("\n1. Add words")
        print("2. View words")
        print("3. Search words")
        print("4. Delete a word")
        print("5. Edit a word")
        print("6. Quiz mode")
        print("7. Statistics")
        print("8. Exit")

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
            edit_word()
        elif choice == "6":
            quiz_words()
        elif choice == "7":
            statistics()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
