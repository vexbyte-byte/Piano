import json

def midi_note_name(midi_num):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (midi_num // 12) - 1
    note = notes[midi_num % 12]
    return f"{note}{octave}"

midi_notes = []
for i in range(128):
    freq = 440 * 2 ** ((i - 69) / 12)
    midi_notes.append({'midi': i, 'name': midi_note_name(i), 'frequency': round(freq, 2)})

with open(fr"E:\others\Music\Keys\database.json", "w") as f:
    json.dump(midi_notes, f, indent=2)

