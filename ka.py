import json
import os
import csv
from datetime import datetime

class ContactBook:
    def __init__(self, filename="contacts.json"):
        self.filename = filename
        self.contacts = []
        self.load_contacts()

    def load_contacts(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                try:
                    self.contacts = json.load(f)
                except json.JSONDecodeError:
                    self.contacts = []
        else:
            self.contacts = []

    def save_contacts(self):
        with open(self.filename, "w") as f:
            json.dump(self.contacts, f, indent=4)

    def add_contact(self, name, phone, email, birthday=None):
        self.contacts.append({
            "name": name,
            "phone": phone,
            "email": email,
            "birthday": birthday,
            "favorite": False
        })
        self.save_contacts()
        print("Contact added.")

    def view_contacts(self):
        if not self.contacts:
            print("No contacts found.")
            return
        for i, c in enumerate(self.contacts, 1):
            fav = "⭐" if c.get("favorite") else ""
            bday = f"🎂 {c['birthday']}" if c.get("birthday") else ""
            print(f"{i}. {c['name']} - {c['phone']} - {c['email']} {fav} {bday}")

    def view_favorites(self):
        favorites = [c for c in self.contacts if c.get("favorite")]
        if not favorites:
            print("No favorite contacts found.")
            return
        print("\nFavorite Contacts:")
        for i, c in enumerate(favorites, 1):
            print(f"{i}. {c['name']} - {c['phone']} - {c['email']} ⭐")

    def search_contact(self, name):
        results = [c for c in self.contacts if name.lower() in c["name"].lower()]
        if not results:
            print("No matches found.")
        else:
            for c in results:
                fav = "⭐" if c.get("favorite") else ""
                bday = f"🎂 {c['birthday']}" if c.get("birthday") else ""
                print(f"{c['name']} - {c['phone']} - {c['email']} {fav} {bday}")

    def delete_contact(self, index):
        if 0 <= index < len(self.contacts):
            removed = self.contacts.pop(index)
            self.save_contacts()
            print(f"Deleted contact: {removed['name']}")
        else:
            print("Invalid contact number.")

    def update_contact(self, index, name=None, phone=None, email=None, birthday=None):
        if 0 <= index < len(self.contacts):
            contact = self.contacts[index]
            contact['name'] = name or contact['name']
            contact['phone'] = phone or contact['phone']
            contact['email'] = email or contact['email']
            contact['birthday'] = birthday or contact.get('birthday')
            self.save_contacts()
            print("Contact updated.")
        else:
            print("Invalid contact number.")

    def mark_favorite(self, index):
        if 0 <= index < len(self.contacts):
            contact = self.contacts[index]
            contact["favorite"] = not contact.get("favorite", False)
            self.save_contacts()
            status = "added to" if contact["favorite"] else "removed from"
            print(f"{contact['name']} {status} favorites.")
        else:
            print("Invalid contact number.")

    # ✅ New Feature 1: Export contacts to CSV
    def export_to_csv(self, csv_filename="contacts.csv"):
        if not self.contacts:
            print("No contacts to export.")
            return
        with open(csv_filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "phone", "email", "birthday", "favorite"])
            writer.writeheader()
            writer.writerows(self.contacts)
        print(f"Contacts exported to '{csv_filename}' successfully.")

    # ✅ New Feature 1: Import contacts from CSV
    def import_from_csv(self, csv_filename="contacts.csv"):
        if not os.path.exists(csv_filename):
            print("CSV file not found.")
            return
        with open(csv_filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["favorite"] = row.get("favorite", "False") in ["True", "true", "1"]
                self.contacts.append(row)
        self.save_contacts()
        print(f"Contacts imported from '{csv_filename}' successfully.")

    # ✅ New Feature 2: Birthday reminders
    def birthday_reminders(self):
        today = datetime.today().strftime("%m-%d")
        birthdays_today = [c for c in self.contacts if c.get("birthday") and c["birthday"][5:] == today]
        if not birthdays_today:
            print("No birthdays today.")
        else:
            print("🎉 Today's Birthdays:")
            for c in birthdays_today:
                print(f"🎂 {c['name']} - {c['birthday']}")

def main():
    book = ContactBook()
    while True:
        print("\nContact Book")
        print("1. View contacts")
        print("2. Add contact")
        print("3. Search contact")
        print("4. Delete contact")
        print("5. Update contact")
        print("6. Mark/Unmark favorite")
        print("7. View favorite contacts")
        print("8. Export to CSV")
        print("9. Import from CSV")
        print("10. Birthday reminders")
        print("11. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            book.view_contacts()
        elif choice == "2":
            name = input("Name: ")
            phone = input("Phone: ")
            email = input("Email: ")
            birthday = input("Birthday (YYYY-MM-DD, optional): ").strip() or None
            book.add_contact(name, phone, email, birthday)
        elif choice == "3":
            query = input("Enter name to search: ")
            book.search_contact(query)
        elif choice == "4":
            book.view_contacts()
            try:
                num = int(input("Enter contact number to delete: ")) - 1
                book.delete_contact(num)
            except ValueError:
                print("Enter a valid number.")
        elif choice == "5":
            book.view_contacts()
            try:
                num = int(input("Enter contact number to update: ")) - 1
                if 0 <= num < len(book.contacts):
                    name = input("New name (leave blank to keep current): ")
                    phone = input("New phone (leave blank to keep current): ")
                    email = input("New email (leave blank to keep current): ")
                    birthday = input("New birthday (YYYY-MM-DD, leave blank to keep current): ").strip() or None
                    book.update_contact(num, name or None, phone or None, email or None, birthday)
                else:
                    print("Invalid contact number.")
            except ValueError:
                print("Enter a valid number.")
        elif choice == "6":
            book.view_contacts()
            try:
                num = int(input("Enter contact number to mark/unmark favorite: ")) - 1
                book.mark_favorite(num)
            except ValueError:
                print("Enter a valid number.")
        elif choice == "7":
            book.view_favorites()
        elif choice == "8":
            filename = input("Enter CSV filename (default: contacts.csv): ").strip() or "contacts.csv"
            book.export_to_csv(filename)
        elif choice == "9":
            filename = input("Enter CSV filename to import (default: contacts.csv): ").strip() or "contacts.csv"
            book.import_from_csv(filename)
        elif choice == "10":
            book.birthday_reminders()
        elif choice == "11":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
