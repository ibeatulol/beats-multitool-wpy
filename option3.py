import requests
import time
import os
import threading

# -------------------------
# Updated ASCII art (By Beat in red)
# -------------------------
ASCII_ART = r"""
   . .       . .       . .       . .    .       . .    .       . .       . .    
.+'|=|`+. .+'|=|`+. .+'|=|`+. .+'|=|`+.=|`+. .+'|=|`+.=|`+. .+'|=|`+. .+'|=|`+. 
|  | `+.| |  | |  | |  | |  | |  | `+ | `+ | |  | `+ | `+ | |  | `+.| |  | |  | 
|  | .    |  |=`++' |  |=|  | |  |  | |  | | |  |  | |  | | |  |=|`.  |  |'. '. 
`+.|=|`+. |  |      |  | |  | |  |  | |  | | |  |  | |  | | |  | `.|  |  | |  | 
.    |  | |  |      |  | |  | |  |  | |  | | |  |  | |  | | |  |    . |  | |  | 
|`+. |  | |  |      |  | |  | |  |  | |  | | |  |  | |  | | |  | .+'| |  | |  | 
`+.|=|.+' `+.|      `+.| |..| `+.|  |.|  |+' `+.|  |.|  |+' `+.|=|.+' `+.| |.+' 

                            By Beat
"""

# ANSI color codes
ANSI_RED = "\033[31m"
ANSI_WHITE = "\033[97m"
ANSI_RESET = "\033[0m"

# Typing speed — very fast
FAST_DELAY = 0.0008

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def setTitle(title):
    # best-effort terminal title set
    print(f"\033]0;{title}\007", end='', flush=True)

def print_text_slowly(text, color=ANSI_WHITE, delay=FAST_DELAY):
    """
    Print `text` line-by-line with a typing effect.
    Color is an ANSI prefix (e.g. ANSI_RED or ANSI_WHITE).
    We print the color prefix once per line to avoid breaking ANSI sequences.
    """
    lines = text.splitlines()
    for i, line in enumerate(lines):
        # Print color prefix
        print(color, end='', flush=True)
        # Print characters with delay
        for ch in line:
            print(ch, end='', flush=True)
            time.sleep(delay)
        # Reset color and newline
        print(ANSI_RESET, flush=True)

def load_ascii_art_from_file(path="art.txt"):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return None
    return None

def webhspamtitle():
    """Show ASCII art in red, with By Beat also red."""
    external = load_ascii_art_from_file()
    art = external if external else ASCII_ART
    print_text_slowly(art, color=ANSI_RED, delay=FAST_DELAY)

def main():
    print_text_slowly("Returning to main menu...", color=ANSI_WHITE)

def webhookspam():
    setTitle("beats webhookspammer")
    clear()
    webhspamtitle()

    while True:
        print_text_slowly("Webhook link to spam or (q for quit):", color=ANSI_WHITE)
        # Use plain ANSI colored prompt for input
        print(ANSI_WHITE + "-> " + ANSI_RESET, end='', flush=True)
        webhook = input().strip()

        if webhook == 'q':
            print_text_slowly("Exiting...", color=ANSI_WHITE)
            break

        try:
            requests.post(webhook, json={'content': ""})
        except Exception:
            print_text_slowly("[!] Your WebHook is invalid!", color=ANSI_WHITE)
            time.sleep(1)
            clear()
            webhspamtitle()
            continue

        print_text_slowly("\nEnter the message to spam", color=ANSI_WHITE)
        print(ANSI_WHITE + "Message -> " + ANSI_RESET, end='', flush=True)
        message = input()

        print_text_slowly("\nAmount of messages to send", color=ANSI_WHITE)
        print(ANSI_WHITE + "Amount -> " + ANSI_RESET, end='', flush=True)
        try:
            amount = int(input())
        except ValueError:
            print_text_slowly("[!] Invalid amount. Returning to main.", color=ANSI_WHITE)
            time.sleep(1.5)
            main()
            return

        def spam():
            try:
                requests.post(webhook, json={'content': message})
            except Exception as e:
                # Show error as white text
                print_text_slowly(f"Error: {e}", color=ANSI_WHITE)

        for _ in range(amount):
            threading.Thread(target=spam, daemon=True).start()
            time.sleep(0.05)

        clear()
        webhspamtitle()
        print_text_slowly("[!] Webhook has been correctly spammed", color=ANSI_WHITE)
        print(ANSI_WHITE + "\nPress ENTER to exit" + ANSI_RESET, end='', flush=True)
        input()

        # Check if the input is 'q' to quit or run gui.py
        while True:
            print(ANSI_WHITE + "Type 'q' to quit or press ENTER to continue: " + ANSI_RESET, end='', flush=True)
            choice = input().strip()
            if choice == 'q':
                print_text_slowly("Exiting...", color=ANSI_WHITE)
                return
            elif choice == '':
                try:
                    os.system('python gui.py')
                except Exception as e:
                    print_text_slowly(f"Error: {e}", color=ANSI_WHITE)
                break

    main()

if __name__ == "__main__":
    webhookspam()
