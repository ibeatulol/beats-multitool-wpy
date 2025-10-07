import requests
import os
import sys
import re
import shutil
import time

def clear_console():
    if os.name == 'nt':  
        os.system('cls')
    else:  
        os.system('clear')
    time.sleep(0.5)

clear_console()

ASCII_ART = r"""
   . .       . .       .         . .       . .    .       . .       . .    
.+'|=|`+. .+'|=|`+. .+'|      .+'|=|`+. .+'|=|`+.=|`+. .+'|=|`+. .+'|=|`+. 
|  | `+ | |  | `+.| |  |      |  | `+.| |.+' |  | `+.| |  | `+.| |  | |  | 
|  |  | | |  |=|`.  |  |      |  |=|`.       |  |      |  |=|`.  |  |'. '. 
|  |  | | |  | `.|  |  |      |  | `.|       |  |      |  | `.|  |  | |  | 
|  |  | | |  |    . |  |    . |  |    .      |  |      |  |    . |  | |  | 
|  | .+ | |  | .+'| |  | .+'| |  | .+'|      |  |      |  | .+'| |  | |  | 
`+.|=|.+' `+.|=|.+' `+.|=|.+' `+.|=|.+'      |.+'      `+.|=|.+' `+.| |.+' 
"""

ANSI_RED = "\033[31m"
ANSI_WHITE = "\033[97m"
ANSI_RESET = "\033[0m"
FAST_DELAY = 0.0008

def print_slow(text, color=ANSI_WHITE, delay=FAST_DELAY):
    lines = text.splitlines()
    for line in lines:
        print(color, end='')
        for ch in line:
            print(ch, end='', flush=True)
            time.sleep(delay)
        print(ANSI_RESET, flush=True)

def print_green(text):
    print("\033[32m" + text + "\033[0m")

def print_red(text):
    print("\033[31m" + text + "\033[0m")

def print_white(text):
    print("\033[97m" + text + "\033[0m")

def resize_terminal_for_banner():
    min_width = 100
    min_height = 22
    columns, rows = shutil.get_terminal_size()
    if columns < min_width or rows < min_height:
        os.system(f'mode con: cols={min_width} lines={min_height}')

def run(webhook_url):
    try:
        if not re.match(r'https?://[^\s/$.?#].[^\s]*', webhook_url):
            print_red(f"Invalid URL: {webhook_url}")
            return
        response = requests.delete(webhook_url)
        if response.status_code == 204:
            print_green(f"Webhook at {webhook_url} has been deleted!")
        else:
            print_red(f"Failed to delete webhook at {webhook_url}. Status code: {response.status_code}")
    except requests.RequestException as e:
        print_red(f"Error deleting webhook at {webhook_url}: {e}")

def delete_multiple_webhooks():
    print_white("Enter the webhook URLs to delete, one per line. Type 'done' when finished:")
    webhook_urls = []
    while True:
        url = input().strip()
        if url.lower() == 'done':
            break
        webhook_urls.append(url)

    for url in webhook_urls:
        run(url)

def open_new_cmd_window():
    if os.name == "nt" and not os.environ.get("WEBHOOK_DELETER_OPEN"):
        os.environ["WEBHOOK_DELETER_OPEN"] = "1"
        os.system(f'start cmd /k python "{os.path.abspath(__file__)}"')
        sys.exit()

if __name__ == "__main__":
    open_new_cmd_window()
    
    resize_terminal_for_banner()
    print_slow(ASCII_ART, color=ANSI_RED, delay=FAST_DELAY)

    while True:
        print_white("\nOptions:")
        print_white("1. Exit")
        print_white("2. Delete multiple webhooks at once")
        choice = input("\033[97mEnter your choice (1/2): \033[0m").strip()

        if choice == '1':
            print_white("Goodbye!")
            sys.exit()
        elif choice == '2':
            delete_multiple_webhooks()
        else:
            print_red("Invalid choice. Please try again.")
