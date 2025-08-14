from cryptography.fernet import Fernet
import os

KEY_FILE = "secret.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    print("Encryption key generated.")

def load_key():
    if not os.path.exists(KEY_FILE):
        print("No key found. Generate one first.")
        return None
    with open(KEY_FILE, "rb") as f:
        return f.read()

def encrypt_file(filename):
    key = load_key()
    if not key: return
    fernet = Fernet(key)
    with open(filename, "rb") as f:
        data = f.read()
    encrypted = fernet.encrypt(data)
    with open(filename, "wb") as f:
        f.write(encrypted)
    print(f"{filename} encrypted.")

def decrypt_file(filename):
    key = load_key()
    if not key: return
    fernet = Fernet(key)
    with open(filename, "rb") as f:
        data = f.read()
    decrypted = fernet.decrypt(data)
    with open(filename, "wb") as f:
        f.write(decrypted)
    print(f"{filename} decrypted.")

def menu():
    print("\n=== File Encryption Tool ===")
    print("1. Generate key")
    print("2. Encrypt file")
    print("3. Decrypt file")
    print("4. Exit")

def main():
    while True:
        menu()
        choice = input("Choose: ")
        if choice == "1":
            generate_key()
        elif choice == "2":
            encrypt_file(input("Filename: "))
        elif choice == "3":
            decrypt_file(input("Filename: "))
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
