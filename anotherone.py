import random
import string
import math
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
    return len(pwd) * math.log2(pool_size)

def strength_score(pwd, entropy):
    score = 0

    score += min(len(pwd) * 4, 40)

    if any(c.islower() for c in pwd):
        score += 10
    if any(c.isupper() for c in pwd):
        score += 10
    if any(c.isdigit() for c in pwd):
        score += 10
    if any(c in "!@#$%^&*()-_=+[]{};:,.<>?/" for c in pwd):
        score += 10

    score += min(entropy / 2, 20)

    if has_sequence(pwd):
        score -= 15
    if has_repeat_sequence(pwd):
        score -= 10

    return max(0, min(100, int(score)))

def password_strength_label(score):
    if score < 25:
        return "Very Weak"
    if score < 50:
        return "Weak"
    if score < 70:
        return "Moderate"
    if score < 85:
        return "Strong"
    return "Very Strong"

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
        return "Error", 0

    if required_chars:
        for c in required_chars:
            if c not in pool:
                return "Error", 0

    if no_repeats and length > len(pool):
        return "Error", 0

    while True:
        try:
            chars = []
            if required_chars:
                chars += list(required_chars)
            chars += random.sample(letters_lower, min_lower)
            chars += random.sample(letters_upper, min_upper)
            chars += random.sample(digits, min_digits)
            chars += random.sample(special, min_special)
        except ValueError:
            return "Error", 0

        if len(chars) > length:
            return "Error", 0

        used = set(chars)
        for _ in range(length - len(chars)):
            options = pool if not no_repeats else ''.join(c for c in pool if c not in used)
            if not options:
                return "Error", 0
            c = random.choice(options)
            chars.append(c)
            used.add(c)

        random.shuffle(chars)
        pwd = "".join(chars)

        if avoid_repeat_sequences and has_repeat_sequence(pwd):
            continue
        if not has_sequence(pwd):
            return pwd, len(pool)

def main():
    print("Random Password Generator")

    while True:
        try:
            count = int(input("How many passwords: "))
            length = int(input("Password length: "))
            min_lower = int(input("Minimum lowercase: "))
            min_upper = int(input("Minimum uppercase: "))
            min_digits = int(input("Minimum digits: "))
            min_special = int(input("Minimum special: "))
        except ValueError:
            print("Invalid input.")
            continue

        exclude_ambiguous = input("Exclude ambiguous? (y/n): ").lower() == "y"
        no_repeats = input("No repeats? (y/n): ").lower() == "y"
        avoid_repeat_sequences = input("Avoid sequences? (y/n): ").lower() == "y"

        blocked = set(input("Block characters (optional): ")) or None
        allowed_only = set(input("Allow only characters (optional): ")) or None
        required = set(input("Must contain characters (optional): ")) or None

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
            score = strength_score(pwd, entropy)
            label = password_strength_label(score)
            results.append((pwd, score, label))

        print("\nGenerated Passwords:\n")
        for i, (p, s, l) in enumerate(results, 1):
            print(f"{i}: {p} | Score: {s}/100 | {l}")

        try:
            pyperclip.copy("\n".join(p for p, _, _ in results))
        except:
            pass

        if input("\nGenerate again? (y/n): ").lower() != "y":
            break

if __name__ == "__main__":
    main()
