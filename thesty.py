import random
import string

def show_menu():
    print("🔐 Password Generator")
    print("1. Letters only")
    print("2. Letters & digits")
    print("3. Letters, digits & symbols")

def generate_password(length, charset):
    return ''.join(random.choice(charset) for _ in range(length))

def main():
    while True:
        show_menu()
        choice = input("Choose option (1/2/3): ")
        
        try:
            length = int(input("Enter password length: "))
        except ValueError:
            print("⚠️ Invalid length.")
            continue

        if choice == '1':
            chars = string.ascii_letters
        elif choice == '2':
            chars = string.ascii_letters + string.digits
        elif choice == '3':
            chars = string.ascii_letters + string.digits + string.punctuation
        else:
            print("⚠️ Invalid choice.")
            continue

        password = generate_password(length, chars)
        print(f"🔑 Your password: {password}")

        again = input("Generate another? (y/n): ").lower()
        if again != 'y':
            print("👋 Goodbye!")
            break

if __name__ == "__main__":
    main()
