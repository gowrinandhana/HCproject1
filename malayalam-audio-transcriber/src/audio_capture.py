# src/audio_capture.py

import sounddevice as sd
import soundfile as sf

def record_audio(duration, filename, samplerate=16000):
    print(f"Recording for {duration} seconds...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()
    sf.write(filename, recording, samplerate)
