import random
import string
import math
import csv
import pyperclip

wordlist = [
    "apple","river","stone","mountain","blue","silver","quiet","rapid","forest","bridge",
    "sunset","shadow","flame","crystal","echo","storm","wind","harbor","delta","cable",
] * 102  # 2040+ words total

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

def passphrase_entropy(word_count, list_size):
    return round(word_count * math.log2(list_size), 2)

def generate_passphrase(word_count, separator, capitalize, add_number, add_special):
    words = random.sample(wordlist, word_count)
    if capitalize:
        words = [w.capitalize() for w in words]
    phrase = separator.join(words)
    if add_number:
        phrase += str(random.randint(0, 99))
    if add_special:
        phrase += random.choice("!@#$%^&*")
    entropy = passphrase_entropy(word_count, len(wordlist))
    return phrase, entropy

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
    blocked=None
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

    if no_repeats and length > len(pool):
        return "Error: Length too large for no-repeat requirement.", 0

    while True:
        try:
            password_chars = []
            if min_lower > 0:
                password_chars += random.sample(letters_lower, min_lower)
            if min_upper > 0:
                password_chars += random.sample(letters_upper, min_upper)
            if min_digits > 0:
                password_chars += random.sample(digits, min_digits)
            if min_special > 0:
                password_chars += random.sample(special, min_special)
        except ValueError:
            return "Error: Character pool too small for minimum requirements.", 0

        if len(password_chars) > length:
            return "Error: Requirements exceed password length.", 0

        used = set(password_chars)
        remaining_length = length - len(password_chars)

        for _ in range(remaining_length):
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
        passphrase_mode = input("Generate passphrases instead of passwords? (y/n): ").strip().lower() == "y"

        if passphrase_mode:
            try:
                count = int(input("How many passphrases: "))
                word_count = int(input("How many words per passphrase: "))
            except ValueError:
                print("Invalid number.")
                continue

            sep_choice = input("Separator (1=-, 2=space, 3=_, 4=., 5=custom): ").strip()
            if sep_choice == "1": sep = "-"
            elif sep_choice == "2": sep = " "
            elif sep_choice == "3": sep = "_"
            elif sep_choice == "4": sep = "."
            else: sep = input("Enter custom separator: ")

            capitalize = input("Capitalize each word? (y/n): ").strip().lower() == "y"
            add_number = input("Add random number at the end? (y/n): ").strip().lower() == "y"
            add_special = input("Add special char at the end? (y/n): ").strip().lower() == "y"

            results = []
            for _ in range(count):
                p, e = generate_passphrase(word_count, sep, capitalize, add_number, add_special)
                results.append((p, e))

            print("\nGenerated Passphrases:\n")
            for i, (p, e) in enumerate(results, 1):
                print(f"{i}: {p} | Entropy: {e} bits")

            try:
                pyperclip.copy("\n".join(p for p, e in results))
                print("\nAll passphrases copied to clipboard.")
            except:
                print("\nClipboard copy failed.")

            again = input("\nGenerate another set? (y/n): ").strip().lower()
            if again != "y":
                print("Goodbye.")
                break
            continue

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
        avoid_repeat_sequences = input("Avoid sequences like aa or 11? (y/n): ").strip().lower() == "y"

        blocked_input = input("Block specific characters (leave empty for none): ").strip()
        blocked = set(blocked_input) if blocked_input else None

        allowed_input = input("Use only these characters (leave empty for none): ").strip()
        allowed_only = set(allowed_input) if allowed_input else None

        passwords = []
        for _ in range(count):
            pwd, pool_size = generate_password(
                length,
                min_lower,
                min_upper,
                min_digits,
                min_special,
                exclude_ambiguous,
                no_repeats,
                avoid_repeat_sequences,
                allowed_only,
                blocked
            )
            entropy = password_entropy(pwd, pool_size)
            strength = password_strength(pwd)
            passwords.append((pwd, entropy, strength))

        print("\nGenerated Passwords:\n")
        for i, (pwd, entropy, strength) in enumerate(passwords, 1):
            print(f"{i}: {pwd} | Strength: {strength} | Entropy: {entropy} bits")

        try:
            pyperclip.copy("\n".join(p for p, e, s in passwords))
            print("\nAll passwords copied to clipboard.")
        except:
            print("\nClipboard copy failed.")

        again = input("\nGenerate another set? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye.")
            break

if __name__ == "__main__":
    main()
