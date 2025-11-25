import random
import string

def generate_password(
    length=12,
    use_digits=True,
    use_special=True,
    exclude_ambiguous=False,
    no_repeats=False
):
    if length < 4:
        return "Error: Password must be at least 4 characters."

    letters = string.ascii_letters
    digits = string.digits if use_digits else ""
    special = "!@#$%^&*()-_=+[]{};:,.<>?/" if use_special else ""

    ambiguous_chars = "Il1O0o"
    if exclude_ambiguous:
        letters = ''.join(c for c in letters if c not in ambiguous_chars)
        digits = ''.join(c for c in digits if c not in ambiguous_chars)

    pool = letters + digits + special
    if not pool:
        return "Error: No characters available to generate password."

    if no_repeats and length > len(pool):
        return "Error: Length too large for no-repeat requirement."

    password_chars = []
    password_chars.append(random.choice(string.ascii_lowercase))
    password_chars.append(random.choice(string.ascii_uppercase))
    if use_digits:
        password_chars.append(random.choice(string.digits))
    if use_special:
        password_chars.append(random.choice(special))

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
    if any(c.islower() for c in pwd): strength += 1
    if any(c.isupper() for c in pwd): strength += 1
    if any(c.isdigit() for c in pwd): strength += 1
    if any(c in "!@#$%^&*()-_=+[]{};:,.<>?/" for c in pwd): strength += 1

    levels = {1: "Weak", 2: "Moderate", 3: "Strong", 4: "Very Strong"}
    return levels.get(strength, "Very Weak")


def main():
    print("Random Password Generator")
    while True:
        try:
            length = int(input("Enter password length (min 4): "))
            if length < 4:
                print("Password must be at least 4 characters.")
                continue
        except ValueError:
            print("Please enter a valid number.")
            continue

        use_digits = input("Include digits? (y/n): ").strip().lower() == "y"
        use_special = input("Include special characters? (y/n): ").strip().lower() == "y"
        exclude_ambiguous = input("Exclude ambiguous characters (l, I, 1, O, 0)? (y/n): ").strip().lower() == "y"
        no_repeats = input("Disallow repeating characters? (y/n): ").strip().lower() == "y"

        pwd = generate_password(
            length,
            use_digits,
            use_special,
            exclude_ambiguous,
            no_repeats=no_repeats
        )

        print(f"\nGenerated Password: {pwd}")
        print(f"Password Strength: {password_strength(pwd)}\n")

        again = input("Generate another? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye.")
            break


if __name__ == "__main__":
    main()
