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