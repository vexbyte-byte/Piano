import os

# Set the path to your folder
folder = r"E:\\Music\\database_new"  # ← Change this to your folder

# MIDI to note name converter
def midi_to_note_name(note):
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F',
                  'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (note // 12) - 1
    name = note_names[note % 12]
    return f"{name}{octave}"

# Rename files
for midi_note in range(21, 109):  # A0 to C8
    old_path = os.path.join(folder, f"{midi_note}.mp3")
    if os.path.exists(old_path):
        note_name = midi_to_note_name(midi_note)
        new_path = os.path.join(folder, f"{note_name}.mp3")
        os.rename(old_path, new_path)
        print(f"Renamed {midi_note}.mp3 → {note_name}.mp3")
    else:
        print(f"Missing: {midi_note}.mp3")
