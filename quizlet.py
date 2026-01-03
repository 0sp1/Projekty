import csv
action = input("Would you like to add a word(Y/n)").strip().lower()

if action == "y":
    with open("word.csv", "a") as csvfile:
        fieldnames = ["word", "translation"]
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)

        writer.writeheader()
        word = input("Add a word ")
        translation = input("And translation ")
        writer.writerow({"word": word, "translation": translation})
        