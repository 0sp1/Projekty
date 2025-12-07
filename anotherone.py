import random
import string
import pyperclip

def generate_password(
    length,
    min_lower,
    min_upper,
    min_digits,
    min_special,
    exclude_ambiguous=False,
    no_repeats=False
):
    letters_lower = string.ascii_lowercase
    letters_upper = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%^&*()-_=+[]{};:,.<>?/"

    ambiguous_chars = "Il1O0o"
    if exclude_ambiguous:
        letters_lower = ''.join(c for c in letters_lower if c not in ambiguous_chars)
        letters_upper = ''.join(c for c in letters_upper if c not in ambiguous_chars)
        digits = ''.join(c for c in digits if c not in ambiguous_chars)

    pool = letters_lower + letters_upper + digits + special
    if no_repeats and length > len(pool):
        return "Error: Length too large for no-repeat requirement."

    password_chars = []
    password_chars += random.sample(letters_lower, min_lower)
    password_chars += random.sample(letters_upper, min_upper)
    password_chars += random.sample(digits, min_digits)
    password_chars += random.sample(special, min_special)

    if len(password_chars) > length:
        return "Error: Requirements exceed password length."

    used = set(password_chars)
    remaining_length = length - len(password_chars)

    for _ in range(remaining_length):
        options = pool
        if no_repeats:
            options = ''.join(c for c in pool if c not in used)
        if not options:
            return "Error: Not enough characters to complete password."
        ch = random.choice(options)
        password_chars.append(ch)
        used.add(ch)

    random.shuffle(password_chars)
    return "".join(password_chars)

def password_strength(pwd):
    strength = 0
    if any(c.islower() for c in pwd):
        strength += 1
    if any(c.isupper() for c in pwd):
        strength += 1
    if any(c.isdigit() for c in pwd):
        strength += 1
    if any(c in "!@#$%^&*()-_=+[]{};:,.<>?/" for c in pwd):
        strength += 1

    levels = {1: "Weak", 2: "Moderate", 3: "Strong", 4: "Very Strong"}
    return levels.get(strength, "Very Weak")

def main():
    print("Random Password Generator")

    while True:
        try:
            count = int(input("How many passwords to generate: "))
            if count < 1:
                print("Enter at least 1.")
                continue
        except ValueError:
            print("Please enter a valid number.")
            continue

        try:
            length = int(input("Enter password length (min 4): "))
            if length < 4:
                print("Password must be at least 4 characters.")
                continue
        except ValueError:
            print("Please enter a valid number.")
            continue

        try:
            min_lower = int(input("Minimum lowercase characters: "))
            min_upper = int(input("Minimum uppercase characters: "))
            min_digits = int(input("Minimum digits: "))
            min_special = int(input("Minimum special characters: "))
        except ValueError:
            print("Please enter valid numbers.")
            continue

        exclude_ambiguous = input("Exclude ambiguous characters? (y/n): ").strip().lower() == "y"
        no_repeats = input("Disallow repeating characters? (y/n): ").strip().lower() == "y"

        passwords = []
        for _ in range(count):
            pwd = generate_password(
                length,
                min_lower,
                min_upper,
                min_digits,
                min_special,
                exclude_ambiguous,
                no_repeats
            )
            passwords.append(pwd)

        print("\nGenerated Passwords:\n")
        for i, pwd in enumerate(passwords, 1):
            print(f"{i}: {pwd} | Strength: {password_strength(pwd)}")

        try:
            pyperclip.copy("\n".join(passwords))
            print("\nAll passwords copied to clipboard.")
        except:
            print("\nClipboard copy failed.")

        again = input("\nGenerate another set? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye.")
            break

if __name__ == "__main__":
    main()
