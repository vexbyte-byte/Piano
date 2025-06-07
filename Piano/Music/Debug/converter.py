import json
import numpy as np
from scipy.io.wavfile import write
import os
from scipy.signal import butter, lfilter

def lowpass_filter(data, cutoff=200, fs=44100, order=4):
    nyq = 0.5 * fs
    norm_cutoff = cutoff / nyq
    b, a = butter(order, norm_cutoff, btype='low')
    return lfilter(b, a, data)

def generate_piano_like_wave(frequency, duration=2.0, sample_rate=44100, amplitude=32767):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    # --- Section for VERY LOW frequencies (e.g., A0, notes below 50 Hz) ---
    if frequency < 50:
        # Strategy: Pure sine wave or fundamental + very few, perfectly harmonic overtones.
        # Absolutely NO inharmonicity (B=0) for these notes to prevent beating.
        # Fewer harmonics, if any, to keep it clean.
        
        # Option 1: Pure Sine Wave (most effective for beating)
        wave = np.sin(2 * np.pi * frequency * t)
        
        # Option 2: Fundamental + one or two perfectly harmonic overtones (uncomment if Option 1 is too simple)
        # wave = np.zeros_like(t)
        # wave += 1.0 * np.sin(2 * np.pi * frequency * t) # Fundamental
        # if frequency * 2 < 200: # Add second harmonic if it's still low enough
        #     wave += 0.3 * np.sin(2 * np.pi * (frequency * 2) * t) # Pure second harmonic
        # if frequency * 3 < 200: # Add third harmonic
        #     wave += 0.1 * np.sin(2 * np.pi * (frequency * 3) * t) # Pure third harmonic
        
        # Envelope for sub-bass notes - adjusted for slightly longer attack/decay for smoothness
        attack_sub = 0.1 # Slightly longer attack
        decay_sub = 0.3 # Slightly longer decay
        release_sub = duration - (attack_sub + decay_sub)
        sustain_level_sub = 0.7 # Slightly lower sustain
        
        envelope_sub = np.zeros_like(t)
        attack_samples_sub = int(attack_sub * sample_rate)
        decay_samples_sub = int(decay_sub * sample_rate)
        
        envelope_sub[:attack_samples_sub] = np.linspace(0, 1, attack_samples_sub)
        envelope_sub[attack_samples_sub:attack_samples_sub+decay_samples_sub] = np.linspace(1, sustain_level_sub, decay_samples_sub)
        
        release_start_sub = attack_samples_sub + decay_samples_sub
        if release_start_sub < len(t):
            release_t_sub = np.linspace(0, duration - (release_start_sub / sample_rate), len(t) - release_start_sub)
            # Use a slightly softer exponential decay for very low notes
            envelope_sub[release_start_sub:] = sustain_level_sub * np.exp(-2 * release_t_sub / (duration - (release_start_sub / sample_rate)))

        # Ensure envelope does not exceed array length before multiplication
        if len(envelope_sub) > len(t):
            envelope_sub = envelope_sub[:len(t)]
        wave *= envelope_sub
        
        # Apply a very aggressive low-pass filter for very low frequencies
        # The cutoff is now explicitly tied to the fundamental, ensuring no higher frequencies cause issues.
        # Using a slightly higher order filter for a sharper cutoff.
        wave = lowpass_filter(wave, cutoff=frequency * 1.5, fs=sample_rate, order=6) # Stronger filter
        
        wave = wave / np.max(np.abs(wave)) if np.max(np.abs(wave)) > 0 else wave # Normalize carefully
        wave *= amplitude
        return wave.astype(np.int16)

    # --- Section for LOW to MID frequencies (50 Hz to 200 Hz) ---
    # Inharmonicity (B) is introduced, but kept very small.
    # Fewer harmonics than high frequencies.
    elif frequency < 200:
        # Gradually increase B for notes going higher in this range
        B = 0.00005 + (frequency - 50) * (0.0001 - 0.00005) / (200 - 50) # Linear interpolation for B
        B = min(B, 0.0001) # Cap B value
        
        if frequency < 80:
            amplitudes = [1.0, 0.3, 0.1] # Fundamental + 2 harmonics
        else:
            amplitudes = [1.0, 0.5, 0.25, 0.1] # Fundamental + 3 harmonics

        wave = np.zeros_like(t)
        for i, amp in enumerate(amplitudes):
            n = i + 1
            # Apply inharmonicity. The small B value should minimize beating.
            inharmonic_freq = frequency * n * np.sqrt(1 + B * (n ** 2))
            # No random phase offset for these notes to ensure stability.
            wave += amp * np.sin(2 * np.pi * inharmonic_freq * t) # Phase offset fixed to 0

        # ADSR-like envelope - standard for these notes
        attack = 0.01
        decay = 0.15
        release_duration_ratio = 0.7 
        sustain_level = 0.6

        attack_samples = int(attack * sample_rate)
        decay_samples = int(decay * sample_rate)
        
        remaining_duration_after_attack_decay = duration - (attack + decay)
        if remaining_duration_after_attack_decay <= 0:
            sustain_samples = 0
            release_samples = int(duration * sample_rate) - attack_samples - decay_samples
        else:
            sustain_samples = int(remaining_duration_after_attack_decay * (1 - release_duration_ratio) * sample_rate)
            release_samples = int(remaining_duration_after_attack_decay * release_duration_ratio * sample_rate)

        envelope = np.zeros_like(t)
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        envelope[attack_samples:attack_samples+decay_samples] = np.linspace(1, sustain_level, decay_samples)
        
        sustain_start = attack_samples + decay_samples
        sustain_end = sustain_start + sustain_samples
        if sustain_end > len(t): sustain_end = len(t)
        envelope[sustain_start:sustain_end] = sustain_level

        release_start = sustain_end
        if release_start < len(t):
            release_t_segment = np.linspace(0, duration - (release_start / sample_rate), len(t) - release_start)
            envelope[release_start:] = sustain_level * np.exp(-5 * release_t_segment / (duration - (release_start / sample_rate)))

        if len(envelope) > len(t):
            envelope = envelope[:len(t)]
        wave *= envelope

        # Reduced noise for this range
        noise = np.random.normal(0, 0.001, wave.shape)
        wave += noise
        
        # Apply low-pass filter specifically for this range to gently roll off higher harmonics
        wave = lowpass_filter(wave, cutoff=frequency * 3 if frequency * 3 < 1000 else 1000, fs=sample_rate, order=4)

        wave = wave / np.max(np.abs(wave)) if np.max(np.abs(wave)) > 0 else wave
        wave *= amplitude
        return wave.astype(np.int16)

    # --- Section for HIGH frequencies (200 Hz and above) ---
    # Standard piano inharmonicity and full harmonic content.
    else:
        B = 0.0002 # Original B value
        amplitudes = [1.0, 0.5, 0.25, 0.125] # Original harmonic content

        wave = np.zeros_like(t)
        for i, amp in enumerate(amplitudes):
            n = i + 1
            inharmonic_freq = frequency * n * np.sqrt(1 + B * (n ** 2))
            phase_offset = np.random.uniform(0, 2 * np.pi) # Random phase for richness
            wave += amp * np.sin(2 * np.pi * inharmonic_freq * t + phase_offset)

        # ADSR-like envelope - standard for these notes
        attack = 0.01
        decay = 0.15
        release_duration_ratio = 0.7 
        sustain_level = 0.6

        attack_samples = int(attack * sample_rate)
        decay_samples = int(decay * sample_rate)
        
        remaining_duration_after_attack_decay = duration - (attack + decay)
        if remaining_duration_after_attack_decay <= 0:
            sustain_samples = 0
            release_samples = int(duration * sample_rate) - attack_samples - decay_samples
        else:
            sustain_samples = int(remaining_duration_after_attack_decay * (1 - release_duration_ratio) * sample_rate)
            release_samples = int(remaining_duration_after_attack_decay * release_duration_ratio * sample_rate)

        envelope = np.zeros_like(t)
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        envelope[attack_samples:attack_samples+decay_samples] = np.linspace(1, sustain_level, decay_samples)
        
        sustain_start = attack_samples + decay_samples
        sustain_end = sustain_start + sustain_samples
        if sustain_end > len(t): sustain_end = len(t)
        envelope[sustain_start:sustain_end] = sustain_level

        release_start = sustain_end
        if release_start < len(t):
            release_t_segment = np.linspace(0, duration - (release_start / sample_rate), len(t) - release_start)
            envelope[release_start:] = sustain_level * np.exp(-5 * release_t_segment / (duration - (release_start / sample_rate)))

        if len(envelope) > len(t):
            envelope = envelope[:len(t)]
        wave *= envelope

        # Standard noise for this range
        noise = np.random.normal(0, 0.003, wave.shape)
        wave += noise

        wave = wave / np.max(np.abs(wave)) if np.max(np.abs(wave)) > 0 else wave
        wave *= amplitude
        return wave.astype(np.int16)

def volume_compensation(frequency, ref_freq=440):
    """
    Stronger volume boost for low frequencies, mild reduction for high frequencies.
    """
    if frequency < ref_freq:
        # Boost low frequencies more aggressively, up to ~3x amplitude for very low notes
        boost = 1 + 2 * (ref_freq - frequency) / ref_freq
        return min(boost, 3.0) # cap max boost to prevent clipping
    else:
        # Slightly reduce high frequencies, keep at least 0.5 amplitude
        reduce = 1 - 0.3 * (frequency - ref_freq) / ref_freq
        return max(reduce, 0.5)


json_path = r"E:\\others\\Music\\Keys\\database.json"
output_folder = r"E:\\others\\Music\\Keys\\output_wavs"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

with open(json_path, "r") as f:
    midi_notes = json.load(f)

for note in midi_notes:
    freq = note['frequency']
    name = note['name']
    amp_factor = volume_compensation(freq)
    print(f"Generating {name}.wav with amplitude factor {amp_factor:.2f}")
    wave_data = generate_piano_like_wave(freq, duration=2.0, amplitude=int(32767 * amp_factor))
    def sanitize_filename(name):
        return name.replace("#", "s").replace("/", "-").replace("\\", "-")
    safe_name = sanitize_filename(name)
    filepath = os.path.join(output_folder, f"{safe_name}.wav")
    write(filepath, 44100, wave_data)