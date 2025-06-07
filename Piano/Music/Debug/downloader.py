import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL of the piano lesson page
base_url = "https://www.apronus.com/music/lessons/unit01.htm"

# Folder to save the files
save_dir = "Apronus_Piano_Keys"
os.makedirs(save_dir, exist_ok=True)

# Get HTML
response = requests.get(base_url)
soup = BeautifulSoup(response.content, "html.parser")

# Find all audio elements
audio_urls = []
for audio_tag in soup.find_all("audio"):
    src = audio_tag.get("src")
    if src and (src.endswith(".mp3") or src.endswith(".wav")):
        full_url = urljoin(base_url, src)
        audio_urls.append(full_url)

# Download each file
for url in audio_urls:
    filename = url.split("/")[-1]
    filepath = os.path.join(save_dir, filename)
    print(f"Downloading: {filename}")
    r = requests.get(url)
    with open(filepath, "wb") as f:
        f.write(r.content)

print("\n✅ Done! All piano keys downloaded.")
