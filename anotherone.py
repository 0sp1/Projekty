import random
import string
import math
import csv
import pyperclip

def has_sequence(pwd):
    for i in range(len(pwd) - 2):
        a, b, c = pwd[i], pwd[i+1], pwd[i+2]
        if a.isalpha() and b.isalpha() and c.isalpha():
            if ord(b) == ord(a) + 1 and ord(c) == ord(b) + 1:
                return True
            if ord(b) == ord(a) - 1 and ord(c) == ord(b) - 1:
                return True
        if a.isdigit() and b.isdigit() and c.isdigit():
            if int(b) == int(a) + 1 and int(c) == int(b) + 1:
                return True
            if int(b) == int(a) - 1 and int(c) == int(b) - 1:
                return True
    return False

def has_repeat_sequence(pwd):
    for i in range(len(pwd) - 1):
        if pwd[i] == pwd[i+1]:
            return True
    return False

def filter_chars(chars, allowed_only, blocked):
    if allowed_only:
        chars = ''.join(c for c in chars if c in allowed_only)
    if blocked:
        chars = ''.join(c for c in chars if c not in blocked)
    return chars

def password_entropy(pwd, pool_size):
    if pool_size <= 1:
        return 0
    return round(len(pwd) * math.log2(pool_size), 2)

def generate_password(
    length,
    min_lower,
    min_upper,
    min_digits,
    min_special,
    exclude_ambiguous=False,
    no_repeats=False,
    avoid_repeat_sequences=False,
    allowed_only=None,
    blocked=None,
    required_chars=None
):
    letters_lower = string.ascii_lowercase
    letters_upper = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%^&*()-_=+[]{};:,.<>?/"

    if exclude_ambiguous:
        ambiguous = "Il1O0o"
        letters_lower = ''.join(c for c in letters_lower if c not in ambiguous)
        letters_upper = ''.join(c for c in letters_upper if c not in ambiguous)
        digits = ''.join(c for c in digits if c not in ambiguous)

    letters_lower = filter_chars(letters_lower, allowed_only, blocked)
    letters_upper = filter_chars(letters_upper, allowed_only, blocked)
    digits = filter_chars(digits, allowed_only, blocked)
    special = filter_chars(special, allowed_only, blocked)

    pool = letters_lower + letters_upper + digits + special
    if not pool:
        return "Error: Character pool empty after filters.", 0

    if required_chars:
        for c in required_chars:
            if c not in pool:
                return "Error: Required character not allowed by filters.", 0

    if no_repeats and length > len(pool):
        return "Error: Length too large for no-repeat requirement.", 0

    while True:
        try:
            password_chars = []
            if required_chars:
                password_chars += list(required_chars)
            password_chars += random.sample(letters_lower, min_lower)
            password_chars += random.sample(letters_upper, min_upper)
            password_chars += random.sample(digits, min_digits)
            password_chars += random.sample(special, min_special)
        except ValueError:
            return "Error: Character pool too small for requirements.", 0

        if len(password_chars) > length:
            return "Error: Requirements exceed password length.", 0

        used = set(password_chars)
        remaining = length - len(password_chars)

        for _ in range(remaining):
            options = pool
            if no_repeats:
                options = ''.join(c for c in pool if c not in used)
            if not options:
                return "Error: Not enough characters to complete password.", 0
            c = random.choice(options)
            password_chars.append(c)
            used.add(c)

        random.shuffle(password_chars)
        pwd = "".join(password_chars)

        if avoid_repeat_sequences and has_repeat_sequence(pwd):
            continue
        if not has_sequence(pwd):
            return pwd, len(pool)

def password_strength(pwd):
    s = 0
    if any(c.islower() for c in pwd):
        s += 1
    if any(c.isupper() for c in pwd):
        s += 1
    if any(c.isdigit() for c in pwd):
        s += 1
    if any(c in "!@#$%^&*()-_=+[]{};:,.<>?/" for c in pwd):
        s += 1
    levels = {1: "Weak", 2: "Moderate", 3: "Strong", 4: "Very Strong"}
    return levels.get(s, "Very Weak")

def main():
    print("Random Password Generator")

    while True:
        try:
            count = int(input("How many passwords to generate: "))
            length = int(input("Password length (min 4): "))
            min_lower = int(input("Minimum lowercase: "))
            min_upper = int(input("Minimum uppercase: "))
            min_digits = int(input("Minimum digits: "))
            min_special = int(input("Minimum special: "))
        except ValueError:
            print("Invalid input.")
            continue

        exclude_ambiguous = input("Exclude ambiguous characters? (y/n): ").lower() == "y"
        no_repeats = input("Disallow repeating characters? (y/n): ").lower() == "y"
        avoid_repeat_sequences = input("Avoid aa / 11 sequences? (y/n): ").lower() == "y"

        blocked = input("Block characters (optional): ").strip()
        blocked = set(blocked) if blocked else None

        allowed_only = input("Allow only these characters (optional): ").strip()
        allowed_only = set(allowed_only) if allowed_only else None

        required = input("Must contain these characters (optional): ").strip()
        required = set(required) if required else None

        results = []
        for _ in range(count):
            pwd, pool = generate_password(
                length,
                min_lower,
                min_upper,
                min_digits,
                min_special,
                exclude_ambiguous,
                no_repeats,
                avoid_repeat_sequences,
                allowed_only,
                blocked,
                required
            )
            entropy = password_entropy(pwd, pool)
            results.append((pwd, entropy, password_strength(pwd)))

        print("\nGenerated Passwords:\n")
        for i, (p, e, s) in enumerate(results, 1):
            print(f"{i}: {p} | Strength: {s} | Entropy: {e} bits")

        try:
            pyperclip.copy("\n".join(p for p, _, _ in results))
            print("\nCopied to clipboard.")
        except:
            pass

        if input("\nGenerate again? (y/n): ").lower() != "y":
            break

if __name__ == "__main__":
    main()
