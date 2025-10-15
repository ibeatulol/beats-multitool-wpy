import os
import subprocess
import shutil
import platform
import re

# Your custom ASCII art
ascii_art = r"""              ____  _ __            __
  __ _  __ __/ / /_(_) /____  ___  / /
 /  ' \/ // / / __/ / __/ _ \/ _ \/ / 
/_/_/_/\_,_/_/\__/_/\__/\___/\___/_/  
"""

text_below = "by beat"

# Color half the text purple, half white
def half_purple_half_white(text):
    half_length = len(text) // 2
    return f"\033[95m{text[:half_length]}\033[0m{text[half_length:]}"

# Strip ANSI codes for visible length calculations
def strip_ansi(text):
    return re.sub(r'\033\[\d+m', '', text)

# Print line centered, accounting for ANSI codes
def print_centered_colored_line(text, width):
    visible_length = len(strip_ansi(text))
    spaces = max((width - visible_length) // 2, 0)
    print(' ' * spaces + text)

# Display the menu
def print_menu():
    terminal_width = shutil.get_terminal_size().columns

    # Print ASCII art
    for line in ascii_art.splitlines():
        print_centered_colored_line(half_purple_half_white(line), terminal_width)

    # Below art
    print_centered_colored_line(half_purple_half_white(text_below), terminal_width)
    print()

    # Menu options — clean, no padding
    menu_options = [
        "Tools",
        "1. Username Tracker",
        "2. Webhook Delter",
        "3. Webhook Spammer",
        "4. Dos Attack",
        "5. Port Scanner",
        "6. IP Geo Locator",
    ]

    for option in menu_options:
        colored = half_purple_half_white(option)
        print_centered_colored_line(colored, terminal_width)

# Main execution
def main():
    # Get the directory of this script to run other options from here
    script_dir = os.path.dirname(os.path.abspath(__file__))

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_menu()
        choice = input("\nSelect an option: ")

        try:
            file_map = {
                '1': "option1.py",
                '2': "option2.py",
                '3': "option3.py",
                '4': "option4.py",
                '5': "option5.py",
                '6': "option6.py",
                
            }

            if choice in file_map:
                # Build full path to script file in same folder
                target_file = os.path.join(script_dir, file_map[choice])
                subprocess.run(["python", target_file], check=True)
            elif choice == '8':
                print("Exiting Multitool.")
                break
            else:
                print("Invalid choice. Please select a valid option.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
