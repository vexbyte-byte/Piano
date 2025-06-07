import mido

def get_note_name(note_number):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (note_number // 12) - 1
    note = notes[note_number % 12]
    return f"{note}{octave}"

mid = mido.MidiFile(r"E:\others\Music\Midi\Señorita- Shawn Mendes, Camila Cabello.mid")
ticks_per_beat = mid.ticks_per_beat
tempo = 500000
current_time = 0.0
active_notes = {}

merged = mido.merge_tracks(mid.tracks)

for msg in merged:
    current_time += mido.tick2second(msg.time, ticks_per_beat, tempo)
    if msg.type == 'set_tempo':
        tempo = msg.tempo
    elif msg.type == 'note_on' and msg.velocity > 0:
        active_notes[(msg.note, msg.channel)] = current_time
    elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
        key = (msg.note, msg.channel)
        if key in active_notes:
            start_time = active_notes.pop(key)
            duration = current_time - start_time
            note_name = get_note_name(msg.note)
            print(f"Note: {note_name:<4}  Start: {start_time:.3f}s  Duration: {duration:.3f}s")
