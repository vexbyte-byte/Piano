import urllib.request
import os
import requests
from datetime import datetime

base_url = "https://assets.onlinepianist.com/player/sounds/"  # ← change this
output_dir = "E:\Music\database_new"
os.makedirs(output_dir, exist_ok=True)

def func1():
    for midi_note in range(24, 97):  # 24 to 96 inclusive
        filename = f"{midi_note}.mp3"
        url = base_url + filename
        output_path = os.path.join(output_dir, filename)
        try:
            print(f"Downloading {filename}...")
            urllib.request.urlretrieve(url, output_path)
        except Exception as e:
            print(f"Failed to download {filename}: {e}")

def func2():
    url = "https://assets.onlinepianist.com/player/sounds/24.mp3"
    response = requests.get(url)

    if response.headers.get("Content-Type") == "audio/mpeg":
        with open("24.mp3", "wb") as f:
            f.write(response.content)
        print("Downloaded successfully")
    else:
        print("Not an MP3 file!")

def func3():
    base_url = "https://assets.onlinepianist.com/player/sounds/"
    os.makedirs(output_dir, exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Referer": "https://www.onlinepianist.com/virtual-piano"
    }

    for midi_note in range(100, 120):  # 24 to 96 inclusive
        filename = f"{midi_note}.mp3"
        url = base_url + filename
        output_path = os.path.join(output_dir, filename)
        now = datetime.now()
        now = now.strftime("%H:%M:%S")
        print(f"\033[94m{now} \033[92mDownloading {filename}...")
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200 and response.headers.get("Content-Type") in ("audio/mpeg", "audio/mp3"):
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"Saved {filename}")
        else:
            print(f"Failed to download {filename} - status: {response.status_code} content-type: {response.headers.get('Content-Type')}")

    print("All done!")


# func1()
# func2()
func3()
