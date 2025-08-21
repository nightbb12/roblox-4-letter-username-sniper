import os
import time
import random
import string
import requests
from requests.adapters import HTTPAdapter, Retry

NAMES = 10
LENGTH = 4
FILE = 'valid.txt'
BIRTHDAY = '1999-04-20'

session = requests.Session()
retries = Retry(total=5, backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)
session.mount("http://", adapter)

class colors:
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

ascii_art = r"""
 ███▄    █  ██▓  ▄████  ██░ ██ ▄▄▄█████▓ ▄▄▄▄    ▄▄▄▄   
 ██ ▀█   █ ▓██▒ ██▒ ▀█▒▓██░ ██▒▓  ██▒ ▓▒▓█████▄ ▓█████▄ 
▓██  ▀█ ██▒▒██▒▒██░▄▄▄░▒██▀▀██░▒ ▓██░ ▒░▒██▒ ▄██▒██▒ ▄██
▓██▒  ▐▌██▒░██░░▓█  ██▓░▓█ ░██ ░ ▓██▓ ░ ▒██░█▀  ▒██░█▀  
▒██░   ▓██░░██░░▒▓███▀▒░▓█▒░██▓  ▒██▒ ░ ░▓█  ▀█▓░▓█  ▀█▓
░ ▒░   ▒ ▒ ░▓   ░▒   ▒  ▒ ░░▒░▒  ▒ ░░   ░▒▓███▀▒░▒▓███▀▒
░ ░░   ░ ▒░ ▒ ░  ░   ░  ▒ ░▒░ ░    ░    ▒░▒   ░ ▒░▒   ░ 
   ░   ░ ░  ▒ ░░ ░   ░  ░  ░░ ░  ░       ░    ░  ░    ░ 
         ░  ░        ░  ░  ░  ░          ░       ░      
                                              ░       ░                              ░ ░       ░ ░  ░  ░        
"""

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def make_username(length):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def check_username(username):
    url = "https://auth.roblox.com/v1/usernames/validate"
    params = {"request.username": username, "request.birthday": BIRTHDAY}
    r = session.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json()

def username_sniper():
    clear_console()
    print(ascii_art)  # sadece ASCII art gösterilecek

    found = 0
    while found < NAMES:
        try:
            username = make_username(LENGTH)
            data = check_username(username)
            code = data.get("code")

            if code == 0:
                found += 1
                print(f"{colors.OKBLUE}[{found}/{NAMES}] [+] {username} AVAILABLE!{colors.ENDC}", flush=True)
                with open(FILE, "a+", encoding="utf-8") as f:
                    f.write(username + "\n")
            else:
                print(f"{colors.FAIL}[-] {username} is taken{colors.ENDC}", flush=True)

        except Exception as e:
            print(f"{colors.WARNING}[!] Error: {e}{colors.ENDC}", flush=True)

        time.sleep(0.5)

    print(f"\n{colors.OKBLUE}[!] Finished {colors.ENDC}")
    input("\nPress Enter to return to menu...")

def show_menu():
    clear_console()
    print(ascii_art)
    print(colors.OKBLUE + "Option 1 : Roblox 4 Letter Username Sniper" + colors.ENDC)
    print()
    return input(colors.OKBLUE + "Enter your choice: " + colors.ENDC).strip()

if __name__ == "__main__":
    while True:
        choice = show_menu()
        if choice == "1":
            username_sniper()
        else:
            print(colors.FAIL + "Invalid choice!" + colors.ENDC)
            time.sleep(1)
