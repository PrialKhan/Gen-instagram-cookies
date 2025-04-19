import requests
import time
import csv
import os
from getpass import getpass
from colorama import Fore, Style, init

init(autoreset=True)  # Auto-reset color after every print

def create_csv_file():
    folder_name = "Prial ig Cookies"
    os.makedirs(folder_name, exist_ok=True)

    base_filename = "Ok Cookies"
    extension = ".csv"
    filename = os.path.join(folder_name, base_filename + extension)
    i = 1

    while os.path.exists(filename):
        filename = os.path.join(folder_name, f"{base_filename}-{i}{extension}")
        i += 1

    return filename

def save_to_csv(data, filename):
    file_exists = os.path.exists(filename)
    with open(filename, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["Username", "Password", "Cookies"])
        writer.writerow(data)

def login_instagram(username, password):
    session = requests.Session()

    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
        "Referer": "https://www.instagram.com/accounts/login/",
        "X-Requested-With": "XMLHttpRequest"
    })

    session.get("https://www.instagram.com/accounts/login/")
    csrf_token = session.cookies.get_dict().get("csrftoken")

    headers = {
        "User-Agent": session.headers["User-Agent"],
        "X-CSRFToken": csrf_token,
        "Referer": "https://www.instagram.com/accounts/login/",
        "X-Requested-With": "XMLHttpRequest"
    }

    login_data = {
        "username": username,
        "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}",
        "queryParams": {},
        "optIntoOneTap": "false"
    }

    try:
        response = session.post(
            "https://www.instagram.com/accounts/login/ajax/",
            data=login_data,
            headers=headers,
            timeout=10
        )

        res = response.json()
        if res.get("authenticated"):
            cookies = session.cookies.get_dict()
            cookie_string = "; ".join([f"{k}={v}" for k, v in cookies.items()])
            print(f"\n{Fore.GREEN}🍪 Cookie:\n{cookie_string}\n")
            return cookie_string
        elif "user" in res and not res["authenticated"]:
            print(f"{Fore.RED}❌ Username or password is incorrect.")
            return None
        else:
            print(f"{Fore.RED}❌ Login failed.")
            return None
    except Exception as e:
        print(f"{Fore.RED}⚠️ Error: {e}")
        return None

# ──────────────────────────────────────────────
# Start of Script

os.system("clear")

print(Fore.CYAN + "===================================")
print(Fore.MAGENTA + "🔥 Instagram Cookie Extractor v1.0 🔥")
print(Fore.CYAN + "        Coded by Prial Khan")
print(Fore.CYAN + "===================================\n")

success = 0
failed = 0
counter = 1
csv_filename = create_csv_file()

while True:
    print(Fore.YELLOW + f"\n🔐 Account #{counter}")
    username = input(Fore.BLUE + "👤 Enter Instagram username: ").strip()
    password = getpass(Fore.BLUE + "🔑 Enter Instagram password: ").strip()

    cookies = login_instagram(username, password)

    if cookies:
        save_to_csv([username, password, cookies], csv_filename)
        success += 1
        print(Fore.GREEN + "✅ Login Successful! Cookie saved.")
    else:
        failed += 1
        print(Fore.RED + "❌ Login Failed!")

    counter += 1

    # ─ Terminal Counter Display ─
    print(Fore.YELLOW + "\n📊 Stats So Far:")
    print(Fore.GREEN + f"   ✅ Success: {success}")
    print(Fore.RED + f"   ❌ Failed:  {failed}")
    print(Fore.CYAN + f"   🔄 Total Tried: {success + failed}")

    input(Fore.MAGENTA + "\n🔁 Press Enter to continue with another account...")
