import requests
import json
import os

ASCII_ART = r"""
   ____   ____  ____           |  |   ____   ____ _____ _/  |_  ___________
  / ___\_/ __ \/  _ \   ______ |  |  /  _ \_/ ___\\__  \\   __\/  _ \_  __ \
 / /_/  >  ___(  <_> ) /_____/ |  |_(  <_> )  \___ / __ \|  | (  <_> )  | \/
 \___  / \___  >____/          |____/\____/ \___  >____  /__|  \____/|__|
/_____/      \/                                 \/     \/
                                  
"""
FOOTER = "by beat"

RED = "\033[31m"
RESET = "\033[0m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii():
    clear_screen()
    lines = ASCII_ART.strip("\n").splitlines()
    maxw = max(len(l) for l in lines)
    centered_footer = FOOTER.center(maxw)
    print(RED + "\n".join(lines) + "\n" + centered_footer + RESET)

def lookup_ip(ip):
    try:
        if not ip or ip.strip() == "":
            raise ValueError("Invalid IP: input required.")
        url = f"http://ip-api.com/json/{ip}?fields=status,message,query,country,regionName,city,lat,lon,org,timezone,isp,as"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        if data.get("status") != "success":
            raise ValueError(data.get("message", "Invalid IP or query."))
        return data
    except Exception as e:
        print(RED + f"Error looking up IP: {e}" + RESET)
        return None

def display_info(data):
    try:
        print("\n--- IP GEO INFO ---")
        print(f"IP Address   : {data.get('query', '—')}")
        print(f"City         : {data.get('city', '—')}")
        print(f"Region       : {data.get('regionName', '—')}")
        print(f"Country      : {data.get('country', '—')}")
        print(f"Latitude     : {data.get('lat', '—')}")
        print(f"Longitude    : {data.get('lon', '—')}")
        print(f"ISP          : {data.get('isp', '—')}")
        print(f"Org          : {data.get('org', '—')}")
        print(f"AS           : {data.get('as', '—')}")
        print(f"Timezone     : {data.get('timezone', '—')}")
        print("--------------------\n")
    except Exception as e:
        print(RED + f"Error displaying info: {e}" + RESET)

def main():
    try:
        while True:
            print_ascii()
            user = input("Enter IP to locate (or 'q' to quit): ").strip()
            if user.lower() in ('q', 'quit', 'exit'):
                break
            if not user:
                print(RED + "Error: You must enter an IP address." + RESET)
                input("Press Enter to continue...")
                continue
            print(f"\nLooking up IP: {user}...")
            data = lookup_ip(user)
            if data:
                display_info(data)
            input("Press Enter to continue...")
    except Exception as e:
        print(RED + f"Error in main loop: {e}" + RESET)

if __name__ == "__main__":
    main()
