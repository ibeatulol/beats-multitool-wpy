#!/usr/bin/env python3

import requests
import os
import sys
import time
import random

def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    time.sleep(0.5)

clear_console()

ASCII_ART = """
   . .    .       . .       . .       . .       .  .       . .       . .    
.+'|=|`+.=|`+. .+'|=|`+. .+'|=|`+. .+'|=|`+. .+'|  |`.  .+'|=|`+. .+'|=|`+. 
|.+' |  | `+.| |  | |  | |  | |  | |  | `+.| |  | .+ |  |  | `+.| |  | |  | 
     |  |      |  |'. '. |  |=|  | |  |      |  |=|.+'  |  |=|`.  |  |'. '. 
     |  |      |  | |  | |  | |  | |  |      |  |  |`+. |  | `.|  |  | |  | 
     |  |      |  | |  | |  | |  | |  |    . |  |  |  | |  |    . |  | |  | 
     |  |      |  | |  | |  | |  | |  | .+'| |  |  |  | |  | .+'| |  | |  | 
     |.+'      `+.| |.+' `+.| |..| `+.|=|.+' `+.|  |..| `+.|=|.+' `+.| |.+' 
                                                                            
                                By Beat
"""

MENU2 = """
[1] Username Tracker
[2] Quit
"""

SITES = {
    "GitHub": [
        "https://github.com/{username}"
    ],
    "Discord": [
        "https://discord.com/users/{username}",
        "https://discordapp.com/users/{username}",
        "https://discord.com/invite/{username}"
    ],
    "guns.lol": [
        "https://guns.lol/{username}",
        "https://guns.lol/u/{username}",
        "https://guns.lol/@{username}"
    ],
    "SoundCloud": [
        "https://soundcloud.com/{username}"
    ],
    "Spotify": [
        "https://open.spotify.com/user/{username}",
        "https://spotify.com/user/{username}"
    ]
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Beat-Username-Tracker/1.0; +https://beat.local)"
}

TIMEOUT = 7
MAX_RETRIES = 3

def print_white(text=""):
    print("\033[97m" + text + "\033[0m")

def print_green(text=""):
    print("\033[32m" + text + "\033[0m")

def print_red(text=""):
    print("\033[31m" + text + "\033[0m")

def check_url(url, retries=MAX_RETRIES):
    try:
        resp = requests.head(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        if resp.status_code in (405, 501):
            resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        return True, resp.status_code, resp.url, None
    except requests.RequestException as e:
        if retries > 0:
            print_red(f"[!] Error accessing {url}: {e}. Retrying...")
            time.sleep(random.uniform(1, 3))
            return check_url(url, retries - 1)
        else:
            return False, None, None, str(e)

def check_username_on_sites(username):
    print_white(f"\nChecking username: '{username}'\n")
    found_any = False

    for site, patterns in SITES.items():
        site_header_printed = False
        for pat in patterns:
            url = pat.format(username=username)
            ok, status, final, err = check_url(url)
            if not site_header_printed:
                print_white(f"--- {site} ---")
                site_header_printed = True

            if ok:
                if status == 200:
                    print_green(f"[+] {url}  (HTTP {status})")
                    found_any = True
                elif status in (301, 302, 303, 307, 308):
                    print_green(f"[+] {url}  (redirect HTTP {status}) -> {final}")
                    found_any = True
                elif status in (401, 403):
                    print_green(f"[~] {url}  (HTTP {status} — access restricted)")
                    found_any = True
                elif status == 404:
                    print_red(f"[-] {url}  (HTTP 404)")
                else:
                    print_white(f"[?] {url}  (HTTP {status}) -> {final}")
            else:
                if err and "ConnectionResetError" in err:
                    print_red(f"[!] {url}  (error: ConnectionResetError, possibly server-side issue or blocked request)")
                else:
                    print_red(f"[!] {url}  (error: {err})")

            time.sleep(0.15)

    if not found_any:
        print_white("\nNo obvious matches found (200/redirect/restricted).")
    else:
        print_white("\nSome profiles may exist based on HTTP responses above.")

def show_menu_and_get_choice():
    clear_console()
    print_red(ASCII_ART)
    print_white(MENU2)
    try:
        choice = input("\033[97mChoice >> \033[0m").strip()
        return choice
    except (KeyboardInterrupt, EOFError):
        print()
        return "2"

def main():
    while True:
        choice = show_menu_and_get_choice()

        if choice == "1":
            username = input("\033[97muser >> \033[0m").strip()
            if not username:
                print_red("No username entered.")
                input("\nPress Enter to return to the menu...\033[0m")
                continue

            clear_console()
            print_red(ASCII_ART)
            print_white(MENU2)
            check_username_on_sites(username)
            input("\nPress Enter to return to the menu...\033[0m")

        elif choice == "2":
            print_white("Goodbye from Beat.")
            break

        else:
            print_red("Invalid choice — enter 1 or 2.")
            input("\nPress Enter to return to the menu...\033[0m")

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...\033[0m")
