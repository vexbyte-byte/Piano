NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def generate_midi_note_database():
    notes = []
    for midi in range(128):
        name = NOTE_NAMES[midi % 12] + str(midi // 12 - 1)  # C4 is MIDI 60
        freq = 440.0 * (2 ** ((midi - 69) / 12))
        notes.append({
            'midi': midi,
            'name': name,
            'frequency': round(freq, 2)
        })
    return notes

# Example usage
note_db = generate_midi_note_database()
for note in note_db:
    print(note)
