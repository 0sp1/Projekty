import random
import string
import math
import pyperclip

DICTIONARY = {
    "password","admin","user","login","welcome","qwerty","abc","test",
    "letmein","monkey","dragon","football","baseball","master","shadow",
    "sun","moon","star","love","secret","hello","world"
}

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

def has_dictionary_word(pwd):
    p = pwd.lower()
    for w in DICTIONARY:
        if len(w) >= 3 and w in p:
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
    score = min(len(pwd) * 4, 40)
    if any(c.islower() for c in pwd): score += 10
    if any(c.isupper() for c in pwd): score += 10
    if any(c.isdigit() for c in pwd): score += 10
    if any(c in "!@#$%^&*()-_=+[]{};:,.<>?/" for c in pwd): score += 10
    score += min(entropy / 2, 20)
    if has_sequence(pwd): score -= 15
    if has_repeat_sequence(pwd): score -= 10
    if has_dictionary_word(pwd): score -= 20
    return max(0, min(100, int(score)))

def strength_label(score):
    if score < 25: return "Very Weak"
    if score < 50: return "Weak"
    if score < 70: return "Moderate"
    if score < 85: return "Strong"
    return "Very Strong"

def crack_time(entropy, guesses_per_sec):
    seconds = (2 ** entropy) / guesses_per_sec
    units = [
        ("seconds", 60),
        ("minutes", 60),
        ("hours", 24),
        ("days", 365),
        ("years", 1000),
        ("millennia", None)
    ]
    value = seconds
    for name, div in units:
        if div is None or value < div:
            return f"{int(value)} {name}"
        value /= div

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
    required_chars=None,
    no_dictionary=False
):
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%^&*()-_=+[]{};:,.<>?/"

    if exclude_ambiguous:
        amb = "Il1O0o"
        lower = ''.join(c for c in lower if c not in amb)
        upper = ''.join(c for c in upper if c not in amb)
        digits = ''.join(c for c in digits if c not in amb)

    lower = filter_chars(lower, allowed_only, blocked)
    upper = filter_chars(upper, allowed_only, blocked)
    digits = filter_chars(digits, allowed_only, blocked)
    special = filter_chars(special, allowed_only, blocked)

    pool = lower + upper + digits + special
    if not pool:
        return "Error", 0

    while True:
        try:
            chars = []
            if required_chars:
                chars += list(required_chars)
            chars += random.sample(lower, min_lower)
            chars += random.sample(upper, min_upper)
            chars += random.sample(digits, min_digits)
            chars += random.sample(special, min_special)
        except ValueError:
            return "Error", 0

        if len(chars) > length:
            return "Error", 0

        used = set(chars)
        for _ in range(length - len(chars)):
            opts = pool if not no_repeats else ''.join(c for c in pool if c not in used)
            if not opts:
                return "Error", 0
            c = random.choice(opts)
            chars.append(c)
            used.add(c)

        random.shuffle(chars)
        pwd = "".join(chars)

        if avoid_repeat_sequences and has_repeat_sequence(pwd):
            continue
        if has_sequence(pwd):
            continue
        if no_dictionary and has_dictionary_word(pwd):
            continue

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
            continue

        exclude_ambiguous = input("Exclude ambiguous? (y/n): ").lower() == "y"
        no_repeats = input("No repeats? (y/n): ").lower() == "y"
        avoid_seq = input("Avoid sequences? (y/n): ").lower() == "y"
        no_dict = input("No dictionary words? (y/n): ").lower() == "y"

        blocked = input("Block characters (optional): ").strip()
        blocked = set(blocked) if blocked else None

        allowed = input("Allow only characters (optional): ").strip()
        allowed = set(allowed) if allowed else None

        required = input("Must contain characters (optional): ").strip()
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
                avoid_seq,
                allowed,
                blocked,
                required,
                no_dict
            )
            entropy = password_entropy(pwd, pool)
            score = strength_score(pwd, entropy)
            online = crack_time(entropy, 1_000)
            offline = crack_time(entropy, 10_000_000_000)
            results.append((pwd, score, strength_label(score), online, offline))

        for i, (p, s, l, o, f) in enumerate(results, 1):
            print(f"{i}: {p} | {s}/100 | {l} | Online: {o} | Offline: {f}")

        try:
            pyperclip.copy("\n".join(p for p, _, _, _, _ in results))
        except:
            pass

        if input("Generate again? (y/n): ").lower() != "y":
            break

if __name__ == "__main__":
    main()
