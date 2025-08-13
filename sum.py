import random
import string
import os

FILE = "passwords.txt"

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(chars) for _ in range(length))

def save_password(name, password):
    with open(FILE, "a") as file:
        file.write(f"{name}: {password}\n")
    print("Password saved.")

def view_passwords():
    if not os.path.exists(FILE):
        print("No saved passwords yet.")
        return
    with open(FILE, "r") as file:
        print("\n--- Saved Passwords ---")
        print(file.read())

def menu():
    print("\n=== Password Manager ===")
    print("1. Generate new password")
    print("2. View saved passwords")
    print("3. Exit")

def main():
    while True:
        menu()
        choice = input("Choose an option: ")
        if choice == "1":
            name = input("Account/Website name: ")
            try:
                length = int(input("Password length (default 12): ") or 12)
            except ValueError:
                length = 12
            password = generate_password(length)
            print(f"Generated password: {password}")
            if input("Save it? (y/n): ").lower() == "y":
                save_password(name, password)
        elif choice == "2":
            view_passwords()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()