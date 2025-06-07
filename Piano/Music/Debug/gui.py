import mido
import time
import threading
import tkinter as tk

# Build a simple keyboard layout
WHITE_KEYS = ['C', 'D', 'E', 'F', 'G', 'A', 'B'] * 2
KEYS = {}
root = tk.Tk()
root.title("Piano Tutor")

frame = tk.Frame(root)
frame.pack()

for i in range(14):  # 2 octaves
    key = tk.Label(frame, text=WHITE_KEYS[i % 7], width=5, height=10, bg='white', relief='raised')
    key.grid(row=0, column=i, padx=1)
    KEYS[60 + i] = key  # Starting from middle C (note 60)

# Function to simulate GUI piano press
def press_key(note):
    if note in KEYS:
        KEYS[note].config(bg='red')

def release_key(note):
    if note in KEYS:
        KEYS[note].config(bg='white')

# Play and update GUI from MIDI
def play_midi(filename):
    mid = mido.MidiFile(filename)
    for msg in mid.play():
        if msg.type == 'note_on' and msg.velocity > 0:
            press_key(msg.note)
        elif msg.type in ['note_off', 'note_on'] and msg.velocity == 0:
            release_key(msg.note)

# Run MIDI playback in separate thread so GUI stays responsive
threading.Thread(target=play_midi, args=('your_song.mid',), daemon=True).start()
root.mainloop()