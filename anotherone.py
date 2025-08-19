import random
import string

def generate_password(length=12, use_digits=True, use_special=True):
    letters = string.ascii_letters
    digits = string.digits if use_digits else ""
    special = "!@#$%^&*()-_=+[]{};:,.<>?/" if use_special else ""
    
    pool = letters + digits + special
    if not pool:
        return "⚠️ No characters available to generate password!"
    
    return "".join(random.choice(pool) for _ in range(length))

def password_strength(pwd):
    strength = 0
    if any(c.islower() for c in pwd): strength += 1
    if any(c.isupper() for c in pwd): strength += 1
    if any(c.isdigit() for c in pwd): strength += 1
    if any(c in "!@#$%^&*()-_=+[]{};:,.<>?/" for c in pwd): strength += 1
    
    levels = {1: "Weak 😢", 2: "Moderate 🙂", 3: "Strong 💪", 4: "Very Strong 🔥"}
    return levels.get(strength, "Very Weak")

def main():
    print("🔐 Random Password Generator 🔐")
    while True:
        try:
            length = int(input("Enter password length (min 4): "))
            if length < 4:
                print("⚠️ Password must be at least 4 characters.")
                continue
        except ValueError:
            print("⚠️ Please enter a valid number.")
            continue

        use_digits = input("Include digits? (y/n): ").strip().lower() == "y"
        use_special = input("Include special chars? (y/n): ").strip().lower() == "y"

        pwd = generate_password(length, use_digits, use_special)
        print(f"\nGenerated Password: {pwd}")
        print(f"Password Strength: {password_strength(pwd)}\n")

        again = input("Generate another? (y/n): ").strip().lower()
        if again != "y":
            print("👋 Stay safe online!")
            break

if __name__ == "__main__":
    main()
