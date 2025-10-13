import json
import os

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

    def add_contact(self, name, phone, email):
        self.contacts.append({"name": name, "phone": phone, "email": email})
        self.save_contacts()
        print("Contact added.")

    def view_contacts(self):
        if not self.contacts:
            print("No contacts found.")
            return
        for i, c in enumerate(self.contacts, 1):
            print(f"{i}. {c['name']} - {c['phone']} - {c['email']}")

    def search_contact(self, name):
        results = [c for c in self.contacts if name.lower() in c["name"].lower()]
        if not results:
            print("No matches found.")
        else:
            for c in results:
                print(f"{c['name']} - {c['phone']} - {c['email']}")

    def delete_contact(self, index):
        if 0 <= index < len(self.contacts):
            removed = self.contacts.pop(index)
            self.save_contacts()
            print(f"Deleted contact: {removed['name']}")
        else:
            print("Invalid contact number.")

    def update_contact(self, index, name=None, phone=None, email=None):
        if 0 <= index < len(self.contacts):
            contact = self.contacts[index]
            contact['name'] = name or contact['name']
            contact['phone'] = phone or contact['phone']
            contact['email'] = email or contact['email']
            self.save_contacts()
            print("Contact updated.")
        else:
            print("Invalid contact number.")

def main():
    book = ContactBook()
    while True:
        print("\nContact Book")
        print("1. View contacts")
        print("2. Add contact")
        print("3. Search contact")
        print("4. Delete contact")
        print("5. Update contact")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            book.view_contacts()
        elif choice == "2":
            name = input("Name: ")
            phone = input("Phone: ")
            email = input("Email: ")
            book.add_contact(name, phone, email)
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
                    book.update_contact(num, name or None, phone or None, email or None)
                else:
                    print("Invalid contact number.")
            except ValueError:
                print("Enter a valid number.")
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
