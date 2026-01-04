import csv
import os

filename = "word.csv"

action = input("Would you like to add a word (Y/n)? ").strip().lower()

if action == "y":
    file_exists = os.path.isfile(filename)

    with open(filename, "a", newline="") as csvfile:
        fieldnames = ["word", "translation"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header only if file does not exist yet
        if not file_exists:
            writer.writeheader()

        while True:
            word = input("Add a word: ").strip()
            translation = input("Add its translation: ").strip()

            writer.writerow({"word": word, "translation": translation})

            more = input("Add another word? (Y/n): ").strip().lower()
            if more != "y":
                break

    print("Words saved successfully!")
