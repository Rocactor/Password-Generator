"""
Password Generator 
𖤛 By Rocactor Team
"""

import os
import sys
import time
import string
import secrets

try:
    from colorama import init, Fore, Style
    import pyfiglet
except ImportError:
    print("𖤛 Installing required libraries ...")
    os.system(f"{sys.executable} -m pip install colorama pyfiglet --quiet")
    from colorama import init, Fore, Style
    import pyfiglet

init(autoreset=True)

COLORS = [Fore.CYAN, Fore.GREEN, Fore.MAGENTA, Fore.YELLOW, Fore.BLUE, Fore.RED]


def clear():
    os.system("clear" if os.name == "posix" else "cls")


def type_effect(text, color=Fore.GREEN, delay=0.015):
    for ch in text:
        sys.stdout.write(color + ch + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def loading_bar(label="Processing", length=28, delay=0.02):
    for i in range(length + 1):
        percent = int((i / length) * 100)
        bar = "█" * i + "░" * (length - i)
        color = COLORS[i % len(COLORS)]
        sys.stdout.write(f"\r{color}{label} [{bar}] {percent}%{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(delay)
    print()


def animated_banner():
    clear()
    banner = pyfiglet.figlet_format("PASS GEN", font="slant")
    lines = banner.split("\n")
    for i, line in enumerate(lines):
        color = COLORS[i % len(COLORS)]
        print(color + line + Style.RESET_ALL)
        time.sleep(0.04)
    type_effect("        Password Generator | 𖤛 By Rocactor Team", Fore.YELLOW, 0.01)
    print()


def box_panel(title, lines, color=Fore.CYAN):
    width = max(len(title), max((len(l) for l in lines), default=0)) + 8
    print(color + "╔" + "═" * width + "╗" + Style.RESET_ALL)
    print(color + "║" + title.center(width) + "║" + Style.RESET_ALL)
    print(color + "╠" + "═" * width + "╣" + Style.RESET_ALL)
    for l in lines:
        print(color + "║ " + l.ljust(width - 1) + "║" + Style.RESET_ALL)
    print(color + "╚" + "═" * width + "╝" + Style.RESET_ALL)


def menu():
    box_panel("Main Panel - Password Generator (Rocactor Team)", [
        "1) Generate a single password",
        "2) Generate multiple passwords",
        "3) Save the last generated password(s) to a file",
        "4) Exit",
    ], Fore.CYAN)


def strength_of(pw):
    score = 0
    if len(pw) >= 12:
        score += 1
    if any(c.islower() for c in pw):
        score += 1
    if any(c.isupper() for c in pw):
        score += 1
    if any(c.isdigit() for c in pw):
        score += 1
    if any(c in string.punctuation for c in pw):
        score += 1
    labels = {0: ("Weak", Fore.RED), 1: ("Weak", Fore.RED), 2: ("Medium", Fore.YELLOW),
              3: ("Good", Fore.YELLOW), 4: ("Strong", Fore.GREEN), 5: ("Very Strong", Fore.GREEN)}
    return labels[score]


def ask_int(prompt, default):
    raw = input(prompt).strip()
    if raw == "":
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def ask_yes(prompt, default=True):
    raw = input(prompt).strip().lower()
    if raw == "":
        return default
    return raw in ("y", "yes", "1")


def build_charset(use_lower, use_upper, use_digits, use_symbols):
    charset = ""
    if use_lower:
        charset += string.ascii_lowercase
    if use_upper:
        charset += string.ascii_uppercase
    if use_digits:
        charset += string.digits
    if use_symbols:
        charset += "!@#$%^&*()-_=+[]{};:,.<>?/"
    return charset


def generate_password(length, charset):
    return "".join(secrets.choice(charset) for _ in range(length))


last_generated = []


def option_single():
    clear()
    box_panel("Generate a Single Password", ["Enter your password settings"], Fore.MAGENTA)
    length = ask_int("Password length (default 16): ", 16)
    use_lower = ask_yes("Include lowercase letters? (Y/n): ", True)
    use_upper = ask_yes("Include uppercase letters? (Y/n): ", True)
    use_digits = ask_yes("Include digits? (Y/n): ", True)
    use_symbols = ask_yes("Include special symbols? (Y/n): ", True)

    charset = build_charset(use_lower, use_upper, use_digits, use_symbols)
    if not charset:
        print(Fore.RED + "At least one character type must be selected!")
        return

    loading_bar("Generating password")
    pw = generate_password(length, charset)
    label, color = strength_of(pw)
    last_generated.clear()
    last_generated.append(pw)

    box_panel("Result", [f"Password: {pw}", f"Strength: {label}"], color)


def option_multiple():
    clear()
    count = ask_int("How many passwords to generate? (default 5): ", 5)
    length = ask_int("Length of each password (default 16): ", 16)
    charset = build_charset(True, True, True, True)
    loading_bar("Generating password list")
    last_generated.clear()
    lines = []
    for i in range(count):
        pw = generate_password(length, charset)
        last_generated.append(pw)
        lines.append(f"{i+1}) {pw}")
    box_panel(f"{count} passwords generated", lines, Fore.GREEN)


def option_save():
    if not last_generated:
        print(Fore.RED + "No password has been generated yet.")
        return
    path = input("File path to save (default passwords.txt): ").strip() or "passwords.txt"
    with open(path, "a", encoding="utf-8") as f:
        for pw in last_generated:
            f.write(pw + "\n")
    loading_bar("Saving")
    print(Fore.GREEN + f"Saved to: {path}")


def main():
    animated_banner()
    while True:
        menu()
        choice = input(Fore.CYAN + "\nChoose an option (1-4): " + Style.RESET_ALL).strip()
        if choice == "1":
            option_single()
        elif choice == "2":
            option_multiple()
        elif choice == "3":
            option_save()
        elif choice == "4":
            type_effect("Goodbye! - 𖤛 Rocactor Team Always The Best.", Fore.YELLOW)
            break
        else:
            print(Fore.RED + "Invalid option.")
        input(Fore.CYAN + "\nPress Enter to continue..." + Style.RESET_ALL)
        animated_banner()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n" + Fore.YELLOW + "Exited.")
