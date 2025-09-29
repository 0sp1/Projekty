import json
import os

class Contact:
    def __init__(self, name, phone, email=""):
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {"name": self.name, "phone": self.phone, "email": self.email}

    @staticmethod
    def from_dict(data):
        return Contact(data["name"], data["phone"], data.get("email", ""))

class ContactBook:
    def __init__(self, filename="contacts.json"):
        self.filename = filename
        self.contacts = []
        self.load_contacts()

    def load_contacts(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.contacts = [Contact.from_dict(c) for c in data]

    def save_contacts(self):
        with open(self.filename, "w") as f:
            json.dump([c.to_dict() for c in self.contacts], f, indent=2)

    def add_contact(self, name, phone, email=""):
        self.contacts.append(Contact(name, phone, email))
        self.save_contacts()

    def list_contacts(self):
        if not self.contacts:
            print("No contacts found.")
        for i, c in enumerate(self.contacts, 1):
            print(f"{i}. {c.name} - {c.phone} ({c.email})")

    def search(self, keyword):
        results = [c for c in self.contacts if keyword.lower() in c.name.lower()]
        for c in results:
            print(f"{c.name} - {c.phone} ({c.email})")
        if not results:
            print("No matches found.")

    def delete(self, name):
        original_count = len(self.contacts)
        self.contacts = [c for c in self.contacts if c.name.lower() != name.lower()]
        if len(self.contacts) < original_count:
            print("Contact deleted.")
            self.save_contacts()
        else:
            print("Contact not found.")

    def update_contact(self, name):
        for contact in self.contacts:
            if contact.name.lower() == name.lower():
                print("Leave field blank to keep current value.")
                new_name = input(f"New name [{contact.name}]: ") or contact.name
                new_phone = input(f"New phone [{contact.phone}]: ") or contact.phone
                new_email = input(f"New email [{contact.email}]: ") or contact.email

                contact.name = new_name
                contact.phone = new_phone
                contact.email = new_email

                self.save_contacts()
                print("Contact updated.")
                return
        print("Contact not found.")

def menu():
    book = ContactBook()
    while True:
        print("\nContact Book")
        print("1. Add Contact")
        print("2. List Contacts")
        print("3. Search Contact")
        print("4. Delete Contact")
        print("5. Exit")
        print("6. Update Contact")
        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Name: ")
            phone = input("Phone: ")
            email = input("Email (optional): ")
            book.add_contact(name, phone, email)
        elif choice == "2":
            book.list_contacts()
        elif choice == "3":
            keyword = input("Enter search keyword: ")
            book.search(keyword)
        elif choice == "4":
            name = input("Enter name to delete: ")
            book.delete(name)
        elif choice == "5":
            break
        elif choice == "6":
            name = input("Enter name of contact to update: ")
            book.update_contact(name)
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    menu()
