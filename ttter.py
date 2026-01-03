contacts = {}

def show_menu():
    print("\nContact Book")
    print("1. Add Contact")
    print("2. View All Contacts")
    print("3. Search Contact")
    print("4. Delete Contact")
    print("5. Exit")

def add_contact():
    name = input("Enter name: ").strip()
    phone = input("Enter phone number: ").strip()
    email = input("Enter email: ").strip()

    if name in contacts:
        print("Contact already exists.")
    else:
        contacts[name] = {"phone": phone, "email": email}
        print("Contact added successfully.")

def view_contacts():
    if not contacts:
        print("No contacts available.")
        return
    for name, info in contacts.items():
        print(f"{name} - Phone: {info['phone']}, Email: {info['email']}")

def search_contact():
    name = input("Enter name to search: ").strip()
    if name in contacts:
        info = contacts[name]
        print(f"{name} - Phone: {info['phone']}, Email: {info['email']}")
    else:
        print("Contact not found.")

def delete_contact():
    name = input("Enter name to delete: ").strip()
    if name in contacts:
        del contacts[name]
        print("Contact deleted successfully.")
    else:
        print("Contact not found.")

def main():
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_contact()
        elif choice == "2":
            view_contacts()
        elif choice == "3":
            search_contact()
        elif choice == "4":
            delete_contact()
        elif choice == "5":
            print("Exiting Contact Book.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
