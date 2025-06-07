# from playsound import playsound

# playsound("E:\\Music\\database_new\\34.mp3")

from mutagen.mp3 import MP3

try:
    audio = MP3("E:\\Music\\database_new\\34.mp3")
    print(f"Length: {audio.info.length} seconds")
except Exception as e:
    print(f"Invalid MP3 or error: {e}")
