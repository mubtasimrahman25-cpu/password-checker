# Password Strength Checker - Step 3
# Checks a password against simple rules, looks for common weak habits,
# and tells the user what to change.
# The program never saves or sends the password anywhere.

import getpass
import string

# A few of the most common passwords. Real lists have thousands.
COMMON_PASSWORDS = {
    "password", "password1", "password123", "123456", "1234567", "12345678",
    "123456789", "1234567890", "qwerty", "qwerty123", "abc123", "letmein",
    "iloveyou", "admin", "welcome", "monkey", "dragon", "football",
    "sunshine", "111111", "000000", "123123",
}

# Runs that people type without thinking
SEQUENCES = [
    "abcdefghijklmnopqrstuvwxyz",
    "0123456789",
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm",
]

# What to tell the user when a rule fails
RULE_ADVICE = {
    "At least 8 characters": "Make it at least 8 characters long.",
    "At least 12 characters": "Make it 12 characters or longer. Length helps the most.",
    "Has lowercase and uppercase letters": "Mix lowercase and uppercase letters.",
    "Has a number": "Add a number.",
    "Has a symbol like ! or @": "Add a symbol like ! or @.",
}


def is_common(password):
    return password.lower() in COMMON_PASSWORDS


def has_repeats(password):
    # Three of the same character in a row, like "aaa" or "111"
    for i in range(len(password) - 2):
        if password[i] == password[i + 1] == password[i + 2]:
            return True
    return False


def has_sequence(password):
    # Three characters in a row from a run, like "abc", "123" or "qwe".
    # Backwards runs like "cba" and "321" count too.
    lower = password.lower()
    for run in SEQUENCES:
        for i in range(len(run) - 2):
            piece = run[i:i + 3]
            if piece in lower or piece[::-1] in lower:
                return True
    return False


def check_password(password):
    # Each rule is a name and True or False.
    rules = {
        "At least 8 characters": len(password) >= 8,
        "At least 12 characters": len(password) >= 12,
        "Has lowercase and uppercase letters": (
            any(c.islower() for c in password) and any(c.isupper() for c in password)
        ),
        "Has a number": any(c.isdigit() for c in password),
        "Has a symbol like ! or @": any(c in string.punctuation for c in password),
    }

    # One point for every rule that passes
    score = sum(1 for passed in rules.values() if passed)

    # Weak habits take points away. Each one is a pair: the problem and the fix.
    warnings = []
    if has_repeats(password):
        warnings.append((
            "Repeats the same character 3 or more times in a row",
            "Avoid repeating a character, like aaa or 111.",
        ))
        score -= 1
    if has_sequence(password):
        warnings.append((
            "Contains an easy run like abc, 123 or qwe",
            "Avoid runs like abc, 123 or qwe.",
        ))
        score -= 1

    # A well-known password is weak no matter how it scores
    if is_common(password):
        warnings.append((
            "This is one of the most common passwords",
            "Pick something that is not on the common lists.",
        ))
        score = 0

    score = max(score, 0)
    return score, rules, warnings


def make_advice(rules, warnings):
    # Collect one tip for every failed rule and every warning
    tips = []
    for name, passed in rules.items():
        if passed:
            continue
        # If it is under 8 characters, the 12 character tip would be repeating itself
        if name == "At least 12 characters" and not rules["At least 8 characters"]:
            continue
        tips.append(RULE_ADVICE[name])

    for problem, fix in warnings:
        tips.append(fix)

    return tips


def rating(score):
    if score <= 1:
        return "Very weak"
    if score == 2:
        return "Weak"
    if score == 3:
        return "Fair"
    if score == 4:
        return "Strong"
    return "Very strong"


def show_result(password):
    score, rules, warnings = check_password(password)
    total = len(rules)

    print("\n--- Result ---")
    for name, passed in rules.items():
        mark = "yes" if passed else "no "
        print(f"[{mark}] {name}")

    if warnings:
        print("\nProblems found:")
        for problem, fix in warnings:
            print(f"  - {problem}")

    bar = "#" * score + "-" * (total - score)
    print(f"\nScore: {score} out of {total}  [{bar}]")
    print(f"Strength: {rating(score)}")

    tips = make_advice(rules, warnings)
    if tips:
        print("\nHow to make it stronger:")
        for tip in tips:
            print(f"  * {tip}")
    else:
        print("\nNothing to fix. This is a strong password.")


def main():
    print("=== Password Strength Checker ===")
    print("Use made-up passwords to test. Do not type a password you really use.")
    print("Nothing shows on screen while you type. That is normal.")

    while True:
        password = getpass.getpass("\nType a password (or press Enter to quit): ")

        if password == "":
            print("Goodbye!")
            break

        show_result(password)


main()
