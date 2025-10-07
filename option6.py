#!/usr/bin/env python3
import os
import socket
import concurrent.futures
import time
import shutil
import sys
import subprocess
from typing import List

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

ASCII_ART = r"""
 ________  ________  ________  ________   ________   _______   ________     
|\   ____\|\   ____\|\   __  \|\   ___  \|\   ___  \|\  ___ \ |\   __  \    
\ \  \___|\ \  \___|\ \  \|\  \ \  \\ \  \ \  \\ \  \ \   __/|\ \  \|\  \   
 \ \_____  \ \  \    \ \   __  \ \  \\ \  \ \  \\ \  \ \  \_|/_\ \   _  _\  
  \|____|\  \ \  \____\ \  \ \  \ \  \\ \  \ \  \\ \  \ \  \_|\ \ \  \\  \| 
    ____\_\  \ \_______\ \__\ \__\ \__\\ \__\ \__\\ \__\ \_______\ \__\\ _\ 
   |\_________\|_______|\|__|\|__|\|__| \|__|\|__| \|__|\|_______|\|__|\|__|
   \|_________|                                                             
                                                                            
                                                                            
"""

# Short list of commonly attacked / high-value ports
PRIORITY_PORTS: List[int] = [
    22, 21, 23, 25, 80, 443, 445, 3389, 3306, 1433, 1521,
    5900, 5432, 6379, 27017, 137, 139, 8080, 8443, 69, 161,
    5000, 2049, 10000
]

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    try:
        width = shutil.get_terminal_size().columns
    except Exception:
        width = 80
    for line in ASCII_ART.splitlines():
        print(RED + line.center(width) + RESET)
    print(RED + "by beat".center(width) + RESET)
    print()

def resolve_host(hostname: str) -> str:
    try:
        for fam, _, _, _, sockaddr in socket.getaddrinfo(hostname, None):
            if fam == socket.AF_INET:
                return sockaddr[0]
        return socket.gethostbyname(hostname)
    except Exception as e:
        raise RuntimeError(f"DNS resolution failed: {e}")

def scan_port(addr: str, port: int, timeout: float) -> tuple[int, bool]:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        res = s.connect_ex((addr, port))
        try:
            s.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        return port, (res == 0)
    except Exception:
        return port, False
    finally:
        try:
            s.close()
        except Exception:
            pass

def run_multitool_bat_and_exit():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bat_path = os.path.join(script_dir, "multitool.bat")
    if not os.path.isfile(bat_path):
        print(RED + f"multitool.bat not found at {bat_path}. Exiting instead." + RESET)
        sys.exit(0)
    try:
        if os.name == "nt":
            subprocess.Popen(["cmd", "/c", "start", "", bat_path], shell=False)
        else:
            subprocess.Popen([bat_path], shell=True)
    except Exception as e:
        print(RED + f"Failed to launch multitool.bat: {e}" + RESET)
    sys.exit(0)

def choose_mode() -> str:
    while True:
        print()
        print("Choose scan mode:")
        print("  01) Full scan (all TCP ports 1-65535)")
        print("  02) Most-hacked ports (priority list)")
        choice = input("Type 01 or 02: ").strip()
        if choice in ("01", "02"):
            return choice
        print(RED + "Invalid choice — type 01 or 02." + RESET)

def print_status(port: int, is_open: bool):
    if is_open:
        # Open: only print the port with [+] in green
        sys.stdout.write(GREEN + f"[+] {port}\n" + RESET)
    else:
        # Closed: print port with [-] in red
        sys.stdout.write(RED + f"[-] {port}\n" + RESET)
    sys.stdout.flush()

def priority_scan(addr: str, threads: int, timeout: float) -> List[int]:
    print(YELLOW + f"\nScanning priority ports ({len(PRIORITY_PORTS)} ports)..." + RESET)
    found = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as ex:
        futures = {ex.submit(scan_port, addr, p, timeout): p for p in PRIORITY_PORTS}
        for fut in concurrent.futures.as_completed(futures):
            port, is_open = fut.result()
            print_status(port, is_open)
            if is_open:
                found.append(port)
    return sorted(found)

def full_scan(addr: str, threads: int, timeout: float, exclude: set) -> List[int]:
    print(YELLOW + "\nScanning all remaining ports (this will print status for every port)..." + RESET)
    CHUNK = 4096
    found = []
    all_ports = [p for p in range(1, 65536) if p not in exclude]
    for i in range(0, len(all_ports), CHUNK):
        chunk = all_ports[i:i+CHUNK]
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as ex:
            futures = {ex.submit(scan_port, addr, p, timeout): p for p in chunk}
            for fut in concurrent.futures.as_completed(futures):
                port, is_open = fut.result()
                print_status(port, is_open)
                if is_open:
                    found.append(port)
        time.sleep(0.15)
    return sorted(found)

def single_scan_flow():
    clear_console()
    print_header()

    target = input("What IP do you want to scan? (default: 127.0.0.1): ").strip() or "127.0.0.1"
    try:
        addr = resolve_host(target)
    except Exception as e:
        print(RED + f"Error: {e}" + RESET)
        return

    print(f"Resolved {target} -> {addr}")

    threads_input = input("Number of threads [default: 200]: ").strip()
    try:
        threads = int(threads_input) if threads_input else 200
    except Exception:
        threads = 200
    if threads < 1:
        threads = 200
    if threads > 800:
        print(YELLOW + "Thread count capped to 800." + RESET)
        threads = 800

    timeout_input = input("Connect timeout seconds [default: 0.5]: ").strip()
    try:
        timeout = float(timeout_input) if timeout_input else 0.5
    except Exception:
        timeout = 0.5

    mode = choose_mode()

    open_ports = []
    start = time.time()

    if mode == "02":
        open_ports = priority_scan(addr, threads, timeout)
    else:  # full scan
        quick_found = priority_scan(addr, threads, timeout)
        open_ports.extend(quick_found)
        exclude = set(PRIORITY_PORTS)
        more_found = full_scan(addr, threads, timeout, exclude)
        open_ports = sorted(set(open_ports) | set(more_found))

    elapsed = time.time() - start

    print()
    if open_ports:
        print(GREEN + f"\nSummary — Open ports ({len(open_ports)}):" + RESET)
        for p in sorted(open_ports):
            sys.stdout.write(GREEN + f"[+] {p}\n" + RESET)
    else:
        print(RED + "No open TCP ports found." + RESET)

    print()
    print(f"Scan duration: {elapsed:.1f} seconds. Done.")

def main():
    while True:
        single_scan_flow()
        # Only two choices: scan again (01) or exit and run multitool.bat (02)
        while True:
            print()
            print("Options:")
            print("  01) Scan again")
            print("  02) Exit and run multitool.bat")
            choice = input("Type 01 or 02 (default 01): ").strip() or "01"
            if choice == "01":
                break
            if choice == "02":
                run_multitool_bat_and_exit()
            print(RED + "Invalid choice — type 01 or 02." + RESET)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nUser cancelled. Exiting.")
        sys.exit(1)
